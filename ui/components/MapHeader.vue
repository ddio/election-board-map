<template lang="pug">
  section
    h2.f5
      span(v-if="visibleCandidates.length === 0")
        | 竟然沒有人有沒看板？！
        call-to-action.normal
      span(v-else-if="isSomeCandidateEmpty").flex.justify-between.items-center
        | 還有 {{regionCandidates.length - visibleCandidates.length}} 位候選人沒看板～
        call-to-action.normal
      span(v-else-if="hasSomeCandidateTooFew").flex.justify-between.items-center
        | 平均每人只有 {{Math.round(avgBoards)}} 個看板？！
        call-to-action.normal
      span(v-else)
        | 這裡有 {{visibleCandidates.length}} 位候選人的 {{visibleBoards.length}} 看板～
</template>
<script>
import { mapGetters } from 'vuex'
import CallToAction from '@/components/CallToAction'

const REPORTED_CAND_LOWER_RATIO = 0.6
const REPORTED_CAND_LOWER_COUNT = 5

export default {
  components: {
    CallToAction,
  },
  computed: {
    ...mapGetters([
      'visibleBoards',
      'visibleCandidates',
      'regionCandidates',
      'isSomeCandidateEmpty',
    ]),
    hasSomeCandidateTooFew () {
      return this.avgBoards <= REPORTED_CAND_LOWER_COUNT
    },
    isSomeCandidateEmpty () {
      return this.visibleCandidates.length === 0 ||
      this.visibleCandidates.length / this.regionCandidates.length <= REPORTED_CAND_LOWER_RATIO
    },
  }
}
</script>
