<template lang="pug">
  main.vh-100.vw-100
    no-ssr
      heat-map(v-if="!onMapReload")
    info-panel
    .headmenu.db.dn-l.absolute.z-999.top-0.w-100
      map-header.bg-white.shadow-1.pa3
    bottom-panel
    nuxt

</template>
<script>
import HeatMap from '@/components/Heatmap'
import InfoPanel from '@/components/InfoPanel'
import BottomPanel from '@/components/BottomPanel'
import MapHeader from '@/components/MapHeader'
import { mapState } from 'vuex'

export default {
  components: {
    HeatMap,
    InfoPanel,
    MapHeader,
    BottomPanel
  },
  computed: {
    ...mapState(['onMapReload'])
  }
}
</script>
<style lang="scss">
.fade-enter-active, .fade-leave-active {
  transition: o
  acity .5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

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

