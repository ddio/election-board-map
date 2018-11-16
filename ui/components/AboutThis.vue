<template lang="pug">
  section.about
    h2.pa3.f5.bb.b--light-gray.flex.justify-between.items-center
      | 關於看板追追追地圖
    .pa3.f6
      p.lh-copy.gray 本網站由 ddio 路過製作，非
        external-link(to="https://www.readr.tw/project/election-board") Readr 看板追追追
        | 專題內容，使用的資料為
        external-link(to="https://www.readr.tw/series/election-board/23") 該專題筆記
        | ，最後更新時間為 2018-11-09，歡迎
        external-link(to="https://github.com/ddio/election-board-map") 分享與改作。
      .flex.justify-center.mt3
        call-to-action.ph4.tc 來讓選舉看板更完整吧！
</template>
<script>
import ExternalLink from '@/components/ExternalLink'
import CallToAction from '@/components/CallToAction'
export default {
  components: {
    ExternalLink,
    CallToAction
  }
}
</script>

<style lang="scss" scoped>
.about {
  p:not(:last-child) {
    margin-bottom: 0.5rem;
  }
}
</style>
