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

export default {
  components: {
    HexGallery
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

