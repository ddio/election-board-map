<template lang="pug">
  .heatmap.h-100
    l-map.heatmap__map(
      ref="map"
      :zoom="zoom"
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
    .heatmap__tooltip.dh.db-l.absolute.bg-white.pa2.ba.b--black-50.w5(v-show="tooltipVisible" :style="tooltipPosition" ref="tooltip")
      .f5.mb2.tc
        strong {{tooltipTitle}}
        | &nbsp;附近
      .f6.tc
        | 有 {{tooltipCandidatesCount}} 位參選人的 {{tooltipPoints.length}} 面看板呦

</template>
<script>
import * as d3 from 'd3'
import boardService from '@/services/boards'
import candidatesService from '@/services/candidates'
import _ from 'lodash'
import { mapMutations } from 'vuex'

const TP_OFFSET = 32

export default {
  props: {
    center: {
      type: Array,
      required: true
    },
    zoom: {
      type: Number,
      required: true
    }
  },
  data () {
    return {
      tooltipPoints: [],
      lastMousePosition: null,
      mapAttribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      mapOptions: {
        zoomControl: false
      }
    }
  },
  computed: {
    mapCenter () {
      return L.latLng(this.center[0], this.center[1])
    },
    tooltipVisible () {
      return this.tooltipPoints.length > 0
    },
    tooltipTitle () {
      if (this.tooltipVisible) {
        return ['county', 'road'].map(key => this.tooltipPoints[0].o[key]).join('')
      }
    },
    tooltipCandidatesCount () {
      if (this.tooltipVisible) {
        const candidates = _.uniq(this.tooltipPoints.map(p => p.o.candidates).flat())
        return candidates.length
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

        const dom = this.$refs.tooltip

        if (xy.x + TP_OFFSET + dom.clientWidth > document.body.clientWidth) {
          xy.x = xy.x - TP_OFFSET - dom.clientWidth
        } else {
          xy.x += TP_OFFSET
        }

        if (xy.y + dom.clientHeight > document.body.clientHeight) {
          xy.y -= dom.clientHeight
        }
      }

      return {
        left: xy.x + 'px',
        top: xy.y + 'px'
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
    ...mapMutations(['mapBound']),
    initHexBin () {
      const candidate_boards = _.map(candidatesService.all(), candidate => candidate.boards_set).flat()
      const points = candidate_boards.map(boardId => boardService.get(boardId))
      const self = this

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
          mouseover (map, data, qq) {
            const e = d3.event
            self.lastMousePosition = {
              x: e.clientX,
              y: e.clientY
            }
            self.tooltipPoints = data
          },
          mouseout: (...args) => {
            this.tooltipPoints = []
          }
        })

      this.hexLayer.data(points)

    },
    onBoundChanged (event) {
      const bound = this.map.getBounds()
      this.$emit('update:bound', bound)
      this.mapBound(bound)
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
