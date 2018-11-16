<template lang="pug">
  external-link.cta.br1.white.ph3.dim.pv1.f6(to="https://www.readr.tw/project/election-board")
    slot 來拍照吧！
</template>
<script>
import ExternalLink from '@/components/ExternalLink'
export default {
  components: {
    ExternalLink
  }
}
</script>
<style lang="scss" scoped>
.cta {
  background: #fa6e59;
  text-decoration: none;
}
</style>

