'use strict'
import Vue from 'vue'
import candidatesService from '@/services/candidates'
import boardService from '@/services/boards'

const typeDict = {
  mayors: '縣市長',
  councilors: '議員'
}

Vue.mixin({
  computed: {
    currentCandidateId () {
      if (this.$route.params.candidate) {
        const result = this.$route.params.candidate.match(/-(\d+)/)
        if (result) {
          return result[1] - 0
        } else {
          return null
        }
      } else {
        return null
      }
    },
    currentCandidate () {
      return candidatesService.get(this.currentCandidateId)
    },
    currentBoardId () {
      if (this.$route.params.board) {
        return this.$route.params.board.match(/(\d+)/)[1] - 0
      } else {
        return null
      }
    },
    currentBoard () {
      return boardService.get(this.currentBoardId)
    },
    currentBoardIndex () {
      if (this.currentBoardId && this.currentCandidateId) {
        const candidate = candidatesService.get(this.currentCandidateId)
        const index = candidate.boards_set.indexOf(this.currentBoardId)

        if (index >= 0) {
          return index
        }
      }
      return 0
    }
  },
  methods: {
    toTypeStr (type) {
      return typeDict[type]
    },
    composeCandidateUrl ({candidateId = null, boardId = null, noBoard = false}) {
      const route = {
        name: '2018-candidate-board',
      }

      candidateId = candidateId || this.currentCandidateId
      boardId = boardId || this.currentBoardId

      const candidate = candidatesService.get(candidateId)
      const candidateToken = `${candidate.name}-${candidateId}`

      if (!candidateId) {
        route.name = '2018'
      } else if (noBoard) {
        route.name = '2018-candidate'
        route.params = {
          candidate: candidateToken
        }
      } else if (boardId) {
        route.params = {
          candidate: candidateToken,
          board: `${boardId}`
        }
      } else {
        route.params = {
          candidate: candidateToken
        }
        if (candidate.boards_set.length > 0) {
          route.params.board = `${candidate.boards_set[0]}`
        } else {
          route.name = '2018-candidate'
        }
      }

      return route
    }
  },
})
