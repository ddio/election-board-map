<template lang="pug">
  .candidate
</template>

<script>
import { mapMutations } from 'vuex'
export default {
  validate ({ params }) {
    return /-\d+$/.test(params.candidate)
  },
  mounted () {
    this.activateCandidate(this.currentCandidateId)
  },
  methods: {
    ...mapMutations(['activateCandidate'])
  }
}
</script>
