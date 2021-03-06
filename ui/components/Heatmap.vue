<template lang="pug">
  .heatmap.h-100
    l-map.heatmap__map(
      ref="map"
      :zoom="mapZoom"
      :center="mapCenter"
      :options="mapOptions"
      @moveend="onBoundChanged"
      @zoomend="onBoundChanged"
    )
      // url="https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}{r}.png"
      // url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      l-tile-layer(
        url="https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}{r}.png"
        :attribution="mapAttribution"
      )
      l-control-zoom(
        position="topright"
      )
      l-marker(
        v-for="(latlng, i) in activeContent.latlngs"
        :key="i"
        :lat-lng="latlng"
        @click="selectActiveBoard(i)"
      )
      l-layer-group(ref="popupWrapper")
        l-popup(
          :lat-lng="popupContent.latlng"
          :options="popupOptions"
        )
          .hexinfo__inner(v-if="popupContent.latlng")
            .hexinfo__title.bb.b--black-10.pa2
              strong {{popupContent.address}}
              | &nbsp;附近
            .pa2.flex.flex-wrap
              .dib.hexinfo__img.bg-center.cover(
                v-for="(img, i) in popupContent.imgs.slice(0,3)"
                :style="{backgroundImage: `url('${img.url}')`}"
                :title="img.alt"
                @click="showHexGallery(i)"
              )
              .dib.hexinfo__img.tc(
                v-show="popupContent.imgs.length > 3"
                title="更多圖片"
                @click="showHexGallery(3)"
              )
                i.fa.fa-ellipsis-h
    hex-gallery(
      :visible.sync="hexGalleryVisible"
      :content="popupContent"
      :galleryIndex.sync="hexGalleryIndex"
    )
    .heatmap__tooltip.dh.db-l.absolute.bg-white.pa2.ba.b--black-50.w5(v-show="tooltipVisible" :style="tooltipPosition" ref="tooltip")
      .f5.mb2.tc
        strong {{tooltipContent.title}}
        | &nbsp;附近
      .f6.tc
        | 有 {{tooltipContent.candidatesCount}} 位參選人的 {{tooltipContent.boardsCount}} 面看板呦

</template>
<script>
import * as d3 from 'd3'
import boardService from '@/services/boards'
import candidatesService from '@/services/candidates'
import _ from 'lodash'
import { mapMutations, mapState, mapGetters } from 'vuex'

import HexGallery from '@/components/HexGallery'

const TP_OFFSET = 32
const TP_W = 256
const TP_H = 100

export default {
  components: {
    HexGallery
  },
  data () {
    return {
      tooltipPoints: [],
      lastMousePosition: null,
      map: null,
      hexLayer: null,
      mapAttribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      mapOptions: {
        zoomControl: false,
        // avoid popup closed when click on hexbin
        closePopupOnClick: false
      },
      popupOptions: {
        className: 'hexinfo',
        maxWidth: 300,
        minWidth: 300
      },
      selectedHexbin: null,
      hexGalleryVisible: false,
      hexGalleryIndex: 0,
    }
  },
  computed: {
    ...mapState(['activeCandidateId', 'mapZoom']),
    ...mapGetters(['mapCenter', 'activeContent']),
    popupContent () {
      if (!this.selectedHexbin) {
        return {}
      }
      const boards = _.uniqBy(this.selectedHexbin.data, (data => data.o.id)).map(bin => bin.o)
      const address = ['county', 'road'].map(key => boards[0][key]).join('')

      const latlng = boards.reduce((sum, board) => {
        sum.lat += board.coordinates[0]
        sum.lng += board.coordinates[1]
        return sum
      }, {lat: 0, lng: 0})

      latlng.lat /= boards.length
      latlng.lng /= boards.length

      const imgs = boards.map(board => {
        return {
          url: boardService.image(board.image),
          alt: `${board.county}${board.road}`
        }
      })

      const relatedPersonIds = _.uniq(
        _.flatten(boards.map(board => board.candidates))
      )
      const relatedPeople = candidatesService.find(relatedPersonIds)
      const mayors = relatedPeople.filter(person => person.type === candidatesService.type.MAYORS)
      const councilors = relatedPeople.filter(person => person.type === candidatesService.type.COUNCILORS)

      return {
        address,
        latlng: L.latLng(latlng.lat, latlng.lng),
        boards,
        imgs,
        mayors,
        councilors
      }
    },
    tooltipVisible () {
      return this.tooltipPoints.length > 0
    },
    tooltipContent () {
      if (!this.tooltipVisible) {
        return {}
      }

      const boards = _.uniqBy(this.tooltipPoints, (data => data.o.id)).map(bin => bin.o)

      const title = ['county', 'road'].map(key => boards[0][key]).join('')
      const candidates = _.uniq(_.flatten(boards.map(board => board.candidates)))

      return {
        title,
        boardsCount: boards.length,
        candidatesCount: candidates.length
      }
    },
    tooltipPosition () {
      const xy = {
        x: 0,
        y: 0
      }
      if (this.tooltipVisible && this.lastMousePosition) {
        xy.x = this.lastMousePosition.x
        xy.y = this.lastMousePosition.y

        if (xy.x + TP_OFFSET + TP_W > document.body.clientWidth) {
          xy.x = xy.x - TP_OFFSET - TP_W
        } else {
          xy.x += TP_OFFSET
        }

        if (xy.y + TP_H > document.body.clientHeight) {
          xy.y -= TP_H
        }
      }

      return {
        left: xy.x + 'px',
        top: xy.y + 'px'
      }
    }
  },
  watch: {
    activeContent () {
      if (this.activeContent.latlngs.length) {
        const lats = this.activeContent.latlngs.map(latlng => latlng.lat)
        const lngs = this.activeContent.latlngs.map(latlng => latlng.lng)
        const maxLat = Math.max(...lats)
        const maxLng = Math.max(...lngs)
        const minLat = Math.min(...lats)
        const minLng = Math.min(...lngs)

        const bounds = L.latLngBounds(
          [minLat, minLng],
          [maxLat, maxLng]
        )

        if (!this.map.getBounds().contains(bounds)) {
          this.map.fitBounds(bounds, {
            padding: [60, 60]
          })
        }
      }
    },
    popupContent (newVal) {
      if (this.popupContent.latlng) {
        this.$nextTick(() => {
          this.$refs.popupWrapper.mapObject.openPopup(this.popupContent.latlng)
          //  this.$refs.popupWrapper.mapObject.openPopup()
          // console.log('OPENED?',
          //   this.$refs.popupWrapper.mapObject.isPopupOpen(),
          //   this.$refs.popupWrapper.mapObject.getPopup()
          // )

          setTimeout(() => {
            console.log('OPENED? 1000+',
              this.$refs.popupWrapper.mapObject.isPopupOpen(),
              this.$refs.popupWrapper.mapObject.getPopup()
            )
          }, 1000)
        })
      }
    }
  },
  mounted () {
    // avoid zoom + move triger this twice
    const realOnBoundChanged = this.onBoundChanged
    this.onBoundChanged = _.debounce(e => {
      realOnBoundChanged(e)
    }, 100)

    this.$nextTick(() => {
      this.initHexBin()
      realOnBoundChanged()
    })
  },
  methods: {
    ...mapMutations(['boundMap']),
    selectActiveBoard (index) {
      this.$router.push(this.composeCandidateUrl({
        boardId: this.activeContent.boards[index].id
      }))
    },
    initHexBin () {
      // check if window width < 60rem
      const isSmallScreen = document.body.clientWidth < 60 * 16

      if (isSmallScreen) {
        this.popupOptions.minWidth = 200
        this.popupOptions.maxWidth = 200
      }

      const candidate_boards = _.flatten(_.map(candidatesService.all(), candidate => candidate.boards_set))
      const points = candidate_boards.map(boardId => boardService.get(boardId))

      const options = {
        opacity: 0.8,
        duration: 500
      }

      this.map = this.$refs.map.mapObject
      this.hexLayer = L.hexbinLayer(options).addTo(this.map)

      this.hexLayer.colorScale().range(['#fff3e0', '#f57c00'])

      this.hexLayer
        .lng(function(d) { return d.coordinates[1] })
        .lat(function(d) { return d.coordinates[0] })
        .hoverHandler({
          mouseover: (map, data, id) => {
            const e = d3.event
            this.lastMousePosition = {
              x: e.clientX,
              y: e.clientY
            }
            this.tooltipPoints = data
          },
          mouseout: (...args) => {
            this.tooltipPoints = []
          }
        })

      this.hexLayer.dispatch().on('click', (data, id) => {
        const e = d3.event
        this.selectedHexbin = {
          data,
          position: {
            x: e.clientX,
            y: e.clientY
          }
        }
      })

      this.hexLayer.data(points)
    },
    onBoundChanged (event) {
      const bound = this.map.getBounds()
      this.$emit('update:bound', bound)
      this.boundMap(bound)
    },
    showHexGallery (imageId) {
      this.hexGalleryVisible = true
      this.hexGalleryIndex = imageId
    },
    hideHexGallery () {
      this.hexGalleryVisible = false
    }
  }
}
</script>
<style lang="scss" scoped>
@import '@/assets/defines.scss';

.heatmap {
  /deep/ .hexbin-hexagon {
    stroke: $primary;
    stroke-width: 1px;
  }

  &__tooltip {
    z-index: 1000;
  }
}
</style>
<style lang="scss">
.hexinfo {
  .leaflet-popup-content-wrapper {
    border-radius: 0.125rem;
  }

  .leaflet-popup-content {
    margin: 0;
  }

  &__inner {
  }

  &__img {
    height: 8rem;
    width: 8rem;
    margin-bottom: 0.25rem;
    opacity: 0.7;
    cursor: pointer;

    &:hover {
      opacity: 0.8;
    }

    &:not(:last-child) {
      margin-right: 0.25rem;
    }

    i {
      font-size: 3rem;
      line-height: 8rem;
    }

    @media screen and (max-width: 60em) {
      height: 4rem;
      width: 4rem;

      i {
        font-size: 2rem;
        line-height: 4rem;
      }
    }
  }
}

.leaflet-right .leaflet-control.leaflet-control-zoom {
  @media screen and (max-width: 60em) {
    margin-top: 4rem;
  }
}

.leaflet-bottom {
  @media screen and (max-width: 60em) {
    bottom: 5.2rem;
  }
}
</style>
