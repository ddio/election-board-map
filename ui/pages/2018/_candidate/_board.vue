<template lang="pug">
  .board
    hex-gallery(
      :visible.sync="activeGalleryVisible"
      :content="activeContent"
      :galleryIndex="currentBoardIndex"
      @update:galleryIndex="nagivateGallery"
    )
</template>
<script>
import { mapMutations, mapState, mapGetters } from 'vuex'
import HexGallery from '@/components/HexGallery'
import boardService from '@/services/boards'

export default {
  components: {
    HexGallery
  },
  head () {
    const board = this.currentBoard
    const cand = this.currentCandidate
    const title = `${board.county}${this.toTypeStr(cand.type)}參選人${cand.name}`
    return {
      title,
      meta: [
        {
          hid: 'description',
          name: 'description',
          content: `${title}-在${board.road}的看板`
        },
        { hid: 'og:image', name: 'og:image', content: boardService.image(board.image)}
      ]
    }
  },
  validate ({ params }) {
    return /^\d+$/.test(params.board)
  },
  data () {
    return {
      activeGalleryVisible: true
    }
  },
  computed: {
    ...mapGetters(['activeContent']),
  },
  watch: {
    activeGalleryVisible () {
      if (!this.activeGalleryVisible) {
        this.$router.push(this.composeCandidateUrl({noBoard: true}))
      }
    }
  },
  mounted () {
    this.activateCandidate(this.currentCandidateId)
    if (this.currentBoardIndex === null) {
      this.activeGalleryVisible = false
    }
  },
  methods: {
    ...mapMutations(['activateCandidate']),
    nagivateGallery (index) {
      this.$router.push(this.composeCandidateUrl({
        boardId: this.activeContent.boards[index].id
      }))
    }
  }
}
</script>

