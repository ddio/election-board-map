<template lang="pug">
  section.dist
    h2.ma0.pa3.f5.bb.b--light-gray.flex.justify-between.items-center
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
      .pa2.bb.b--light-gray.flex.items-center.f6.hover-bg-near-white.pointer(
        v-for="person in people"
        :key="person.id"
        @click="toggleCandidate(person)"
        :class="{'dist--active': isCandidateActive(person)}"
      )
        .ph1.w-30.tc.gray {{person.party}}
        .ph1.w-40.tc {{person.name}}
        .ph1.w-30.tr.orange.dim(title="顯示看板" @click.stop="openBoard(person)")
          | x{{person.boards_set.length}}
          .dn.di-l 看板
          .ml2.dib.pa1
            i.fa.fa-street-view
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
    },
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
    ...mapMutations(['activateCandidate']),
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
      if (this.currentCandidateId && candidate.id === this.currentCandidateId) {
        this.activateCandidate(null)
        this.$router.push({name: '2018'})
      } else {
        this.$router.push(this.composeCandidateUrl({
          candidateId: candidate.id,
          noBoard: true
        }))
      }
    },
    openBoard (candidate) {
      this.$router.push(this.composeCandidateUrl({
        candidateId: candidate.id
      }))
    },
    isCandidateActive (candidate) {
      if (!this.currentCandidateId) {
        return false
      }
      return this.currentCandidateId === candidate.id
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
    max-height: calc(100vh - 26rem);
    overflow: auto;

    @media screen and (max-width: 60em) {
      max-height: calc(26vh);
    }
  }
}
</style>



