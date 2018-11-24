<template lang="pug">
  transition(name="fade")
    .absolute.absolute--fill.flex.items-center.justify-center.bg-black-50.z-9999(v-if="visible && board" @click="closeIt")
      .hexgallery.shadow-5.bg-white.br3.flex.flex-column.mw6-l.w-90(@click.stop)
        .aspect-ratio.aspect-ratio--1x1.bg-center.cover.br3.br--top(
          :style="{backgroundImage: `url('${img.url}')`}"
        )
          .hexgallery__title.absolute.bottom-0.w-100.pa3.pt4.tr.white.f3
            | {{title}} ({{galleryIndex+1}}/{{content.imgs.length}})
          .hexgallery__action.right-0.justify-end(@click="next")
            .dn
              i.fa.fa-chevron-circle-right.white.shadow-1.o-70.mr4
          .hexgallery__action.left-0.justify-start(@click="prev")
            .dn.shadow-2
              i.fa.fa-chevron-circle-left.white.o-70.ml4
          .hexgallery__close.pointer.dim.absolute.pa3.top-0.right-0(@click.stop="closeIt")
            i.fa.fa-close.white
        .pa3
          .dib.f5.ma1(v-for="cand in candidates" :key="cand.key")
            span.gray {{cand.party}}
            span.black {{cand.str}}
        p.tc.pa3.bt.b--black-10.lh-copy
          | 資料有誤？請
          call-to-action.mh1.mb1(to="https://www.facebook.com/messages/t/readr.tw") 私訊 Readr 粉絲頁
          | 或
          call-to-action.mh1(to="mailto:readr@readr.tw") 寫信給 Readr

</template>
<script>
import candidatesService from '@/services/candidates'
import CallToAction from '@/components/CallToAction'
import _ from 'lodash'

export default {
  components: {
    CallToAction
  },
  props: {
    visible: {
      type: Boolean,
      required: true
    },
    content: {
      type: Object,
      required: true,
      validators (content) {
        return _.isArray(content.imgs) && _.isArray(content.boards)
      }
    },
    galleryIndex: {
      type: Number,
      default: 0
    }
  },
  computed: {
    img () {
      if (this.content.imgs.length === 0) {
        return {}
      } else if (this.content.imgs.length <= this.galleryIndex) {
        return this.content.imgs[0]
      } else {
        return this.content.imgs[this.galleryIndex]
      }
    },
    board () {
      if (!this.img.url) {
        return this.content.boards[0]
      } else {
        return this.content.boards[this.galleryIndex]
      }
    },
    title () {
      return ['county', 'district', 'road']
        .map(k => this.board[k])
        .join('')
    },
    candidates () {
      return candidatesService.find(this.board.candidates).map(cand => {
        return {
          party: cand.party,
          str: `${this.toTypeStr(cand.type)}參選人${cand.name}`
        }
      })
    }
  },
  methods: {
    next () {
      if (this.galleryIndex === this.content.boards.length - 1) {
        this.$emit('update:galleryIndex', 0)
      } else {
        this.$emit('update:galleryIndex', this.galleryIndex + 1)
      }
    },
    prev () {
      if (this.galleryIndex === 0) {
        this.$emit('update:galleryIndex', this.content.boards.length - 1)
      } else {
        this.$emit('update:galleryIndex', this.galleryIndex - 1)
      }
    },
    closeIt () {
      this.$emit('update:visible', false)
    }
  }
}
</script>
<style lang="scss" scoped>
.hexgallery {
  &__title {
    background-image: linear-gradient(0deg, #333, transparent);
  }

  &__close {
    font-size: 2rem;
  }

  &__action {
    cursor: pointer;
    position: absolute;
    width: 50%;
    height: 100%;
    display: flex;
    align-items: center;

    i {
      font-size: 4rem;
    }

    &:hover .dn {
      display: block;
    }
  }
}
</style>
