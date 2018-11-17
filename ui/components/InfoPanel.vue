<template lang="pug">
  .info.dn.db-l.z-999.absolute.top-0.left-0(:class="{'info--hidden': !isVisible}")
    .relative.h-100.pr4
      .info__actions.absolute.top-0.pa3.shadow-5.br1.br--right.pointer(@click="toggle" v-show="!duringToggle")
        i.fa.fa-angle-left(v-show="isVisible")
        i.fa.fa-angle-right(v-show="!isVisible")
      transition(name="slide" @after-leave="finishToggle" @after-enter="finishToggle")
        .info__content.pa2.shadow-5.br1.overflow-y-auto(v-show="isVisible")
          map-header.br1.bg-white.shadow-1.pa3.mb2
          board-dist.br1.bg-white.shadow-1.mb2
          about-this.br1.bg-white.shadow-1


</template>
<script>
import MapHeader from '@/components/MapHeader'
import BoardDist from '@/components/BoardDist'
import AboutThis from '@/components/AboutThis'

export default {
  components: {
    BoardDist,
    MapHeader,
    AboutThis
  },
  data () {
    return {
      isVisible: true,
      duringToggle: false
    }
  },
  methods: {
    toggle () {
      this.isVisible = !this.isVisible
      this.duringToggle = true
    },
    finishToggle () {
      this.duringToggle = false
    }
  }
}
</script>
<style lang="scss" scoped>
.info {
  /* to be consistent with leaflet zoom control */
  left: 10px;
  top: 10px;

  &__content {
    background: #fafafa;
    width: 26rem;
    max-height: calc(100vh - 20px);
  }

  &__actions {
    right: calc(-0.5rem + 2px);
    background: #fafafa;
  }

  &--hidden {
    .info__actions {
      right: 10px;
    }
  }
}
</style>
<style lang="scss">
.slide-enter-active, .slide-leave-active {
  transition: 0.5s;
}
.slide-enter, .slide-leave-to {
  transform: translate(-100%, 0);
}
.aaslide-leave-to {
  transform: translate(-100%, 0);
}
</style>
