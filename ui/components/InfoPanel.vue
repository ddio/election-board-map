<template lang="pug">
  .info.h-100.pa2
    map-header.br1.bg-white.shadow-1.pa3.mb2
    board-dist.br1.bg-white.shadow-1.mb2
    about-this.br1.bg-white.shadow-1
</template>
<script>
import CallToAction from '@/components/CallToAction'
import MapHeader from '@/components/MapHeader'
import BoardDist from '@/components/BoardDist'
import AboutThis from '@/components/AboutThis'
import { mapGetters } from 'vuex'

export default {
  components: {
    CallToAction,
    BoardDist,
    MapHeader,
    AboutThis
  },
  computed: {
    ...mapGetters([
      'visibleBoards',
      'visibleCandidates',
      'regionCandidates',
    ])
  }
}
</script>
<style lang="scss" scoped>
.info {
  background: #fafafa;
}
</style>
