import boardService from '@/services/boards'
import candidatesService from '@/services/candidates'
import _ from 'lodash'

export const state = () => {
  return {
    mapBound: null
  }
}

export const mutations = {
  mapBound (state, bound) {
    state.mapBound = bound
  },
}

export const actions = {
}

export const getters = {
  visibleBoards (state) {
    if (!state.mapBound) {
      return []
    }

    const nw = state.mapBound.getNorthWest()
    const se = state.mapBound.getSouthEast()

    return _.filter(boardService.all(), board => {
      return nw.lat >= board.coordinates[0] && se.lat <= board.coordinates[0] &&
        nw.lng <= board.coordinates[1] && se.lng >= board.coordinates[1]
    })
  },
  visibleCandidates (state, getters) {
    const dupCandIds = getters.visibleBoards.map(board => board.candidates)
    const candIds = _.uniq(
      _.flatten(dupCandIds)
    )
    return candidatesService.find(candIds)
  },
  visibleRegions (state, getters) {
    const regions = {
      mayors: {},
      councilors: {}
    }

    getters.visibleCandidates.forEach(cand => {
      if (cand.type === candidatesService.type.MAYORS) {
        regions.mayors[cand.county] = true
      } else if (cand.type === candidatesService.type.COUNCILORS) {
        if (!regions.councilors[cand.county]) {
          regions.councilors[cand.county] = {}
        }

        regions.councilors[cand.county][cand.district] = true
      }
    })

    return regions
  },
  regionCandidates (state, getters) {
    const regions = getters.visibleRegions
    return _.filter(candidatesService.all(), cand => {
      if (cand.type === candidatesService.type.MAYORS) {
        return cand.county in regions.mayors
      } else if (cand.type === candidatesService.type.COUNCILORS) {
        return cand.county in regions.councilors &&
          cand.district in regions.councilors[cand.county]
      }
    })
  },
  avgBoards (state, getters) {
    const totalBoards = getters.visibleCandidates.reduce((sum, cand) => sum + cand.boards_set.length, 0)
    return Math.round(totalBoards / getters.visibleCandidates.length)
  },

}
