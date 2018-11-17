<template lang="pug">
  div
    .panel.bottommenu.db.dn-l.absolute.w-100.ph2.shadow-1(
      :class="{'panel--hidden': !isVisible}"
    )
      .panel__toggle.pointer.tc(@click="toggleIt")
        i.gray.fa.fa-angle-down(v-show="isVisible")
        i.gray.fa.fa-angle-up(v-show="!isVisible")
      board-dist.br1.bg-white.shadow-1.mb2(@click.stop)
      .tr.mt2.mb2
        a.br1.w-100.dib.pr1.pv2.dim.f6.black-70.pointer.underline(@click="showAbout")
          | 關於看板追追追地圖
    transition(name="fade")
      .absolute.absolute--fill.flex.items-center.justify-center.bg-black-50.z-9999(v-if="isAboutVisible" @click="hideAbout")
        .w-90.br1.bg-white.shadow-1(@click.stop)
          about-this
</template>
<script>
import BoardDist from '@/components/BoardDist'
import AboutThis from '@/components/AboutThis'

export default {
  components: {
    BoardDist,
    AboutThis
  },
  data () {
    return {
      isVisible: false,
      isAboutVisible: false
    }
  },
  methods: {
    qqq () {
      console.log('qqq')
    },
    toggleIt () {
      this.isVisible = !this.isVisible
    },
    showAbout () {
      this.isAboutVisible = true
    },
    hideAbout () {
      this.isAboutVisible = false
    }
  }
}
</script>
<style lang="scss" scoped>
.panel {
  z-index: 1001;
  background: #fafafa;
  bottom: 0;

  &--hidden {
    height: 5rem;
    overflow: none;
  }

  &__toggle {
    font-size: 2rem;
  }
}
</style>
