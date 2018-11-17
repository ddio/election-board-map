<template lang="pug">
  section.dist
    h2.pa3.f5.bb.b--light-gray.flex.justify-between.items-center
      div 看板分佈
      .dist__cats.normal.gray
        a.dist__action.pointer.link.dim.br1.ph3.pv1.dib.ba.b--black-20(
          v-show="hasMayors"
          @click="toggleMayors"
          :class="{'dist__action--active': isMayorsSelected}"
        ) 縣市長 ({{nMayors}})
        a.dist__action.pointer.link.dim.br1.ph3.pv1.dib.ba.b--black-20(
          v-show="hasCouncilors"
          @click="toggleCouncilors"
          :class="{'dist__action--active': isCouncilorsSelected}"
        ) 議員 ({{nCouncilors}})
    .dist__body.pa3
      .pa2.bb.b--light-gray.flex.items-center.f6.hover-bg-near-white.pointer.dim(
        v-for="person in people"
        :key="person.id"
        @click="toggleCandidate(person)"
        :class="{'dist--active': isCandidateActive(person)}"
      )
        .ph1.w-30.tc.gray {{person.party}}
        .ph1.w-40.tc {{person.name}}
        .ph1.w-30.tc.orange x{{person.boards_set.length}} 看板
</template>
<script>
import _ from 'lodash'
import { mapGetters, mapMutations } from 'vuex'
import candidatesService from '@/services/candidates'

export default {
  data () {
    return {
      isMayorsSelected: false,
      isCouncilorsSelected: false,
      lastCandidate: null,
    }
  },
  computed: {
    ...mapGetters([
      'visibleBoards',
      'visibleCandidates',
      'regionCandidates',
      'isSomeCandidateEmpty',
    ]),
    nMayors () {
      return this.regionCandidates.filter(cand => cand.type === candidatesService.type.MAYORS).length
    },
    hasMayors () {
      return this.nMayors > 0
    },
    nCouncilors () {
      return this.regionCandidates.filter(cand => cand.type === candidatesService.type.COUNCILORS).length
    },
    hasCouncilors () {
      return this.nCouncilors > 0
    },
    people () {
      const target = this.isMayorsSelected ? candidatesService.type.MAYORS : candidatesService.type.COUNCILORS
      const people = this.regionCandidates.filter(cand => cand.type === target)
      return _.sortBy(people, person => person.boards_set.length * -1)
    }
  },
  watch: {
    hasMayors () {
      this.ensureSthOpened()
    },
    hasCouncilors () {
      this.ensureSthOpened()
    }
  },
  mounted () {
    this.ensureSthOpened()
  },
  methods: {
    ...mapMutations(['activeCandidateId']),
    ensureSthOpened () {
      if (this.hasMayors && !this.hasCouncilors) {
        this.isMayorsSelected = true
        this.isCouncilorsSelected = false
      } else if (!this.hasMayors && this.hasCouncilors) {
        this.isMayorsSelected = false
        this.isCouncilorsSelected = true
      } else if (this.isMayorsSelected === this.isCouncilorsSelected) {
        if (this.hasMayors) {
          this.isMayorsSelected = true
        } else {
          this.isCouncilorsSelected = true
        }
      }
    },
    toggleCandidate (candidate) {
      if (this.lastCandidate && candidate.id === this.lastCandidate.id) {
        this.activeCandidateId(null)
        this.lastCandidate = null
      } else {
        this.activeCandidateId(candidate.id)
        this.lastCandidate = candidate
      }
    },
    isCandidateActive (candidate) {
      if (!this.lastCandidate) {
        return false
      }
      return this.lastCandidate.id === candidate.id
    },
    toggleMayors () {
      if (this.hasCouncilors) {
        this.isCouncilorsSelected = !this.isCouncilorsSelected
        this.isMayorsSelected = !this.isMayorsSelected
      } else {
        this.isMayorsSelected = true
      }
    },
    toggleCouncilors () {
      if (this.hasMayors) {
        this.isCouncilorsSelected = !this.isCouncilorsSelected
        this.isMayorsSelected = !this.isMayorsSelected
      } else {
        this.isCouncilorsSelected = true
      }
    }
  }
}
</script>
<style lang="scss" scoped>
@import '@/assets/defines.scss';

.dist {
  &__action {
    outline: none;

    &--active {
      border-color: $secondary;
      color: $secondary;
      background: $secondary-bg;
    }
  }

  &__action:not(:last-child) {
    margin-right: 0.5rem;
  }

  &--active {
    background: $secondary-bg;
  }

  &__body {
    max-height: calc(100vh - 25rem);
    overflow: auto;

    @media screen and (max-width: 60em) {
      max-height: calc(26vh);
    }
  }
}
</style>



