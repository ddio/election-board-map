<template lang="pug">
  .candidate
</template>

<script>
import { mapMutations } from 'vuex'
import boardService from '@/services/boards'

export default {
  validate ({ params }) {
    return /-\d+$/.test(params.candidate)
  },
  head () {
    const cand = this.currentCandidate
    let board = {image: ''}

    if (cand.boards_set.length > 0) {
      board = boardService.get(cand.boards_set[0])
    }

    const title = `${cand.county}${this.toTypeStr(cand.type)}參選人${cand.name}`

    return {
      title,
      meta: [
        {
          hid: 'description',
          name: 'description',
          content: `${title}`
        },
        { hid: 'og:image', name: 'og:image', content: boardService.image(board.image)}
      ]
    }
  },
  mounted () {
    this.activateCandidate(this.currentCandidateId)
  },
  methods: {
    ...mapMutations(['activateCandidate'])
  }
}
</script>
