<template>
  <div class="common">
    <div class="category-block">
      <div class="incomes">
        <div v-for="income in incomes" :key="income.pk" class="category">
          <div class="category-name">{{limitWordLength(income.description)}}</div>
          <div class="category-balance">{{parseFloat(income.balance).toFixed(2)}}₽</div>
        </div>
        <div class="category">
          <div class="category-name category-add">&#65291;</div>
        </div>
      </div>
      <div class="category-type">Incomes</div>
    </div>
    <div class="arrow">&#x203A;</div>
    <div class="category-block">
      <div class="assets">
        <div v-for="asset in assets" :key="asset.pk" class="category">
          <div class="category-name">{{limitWordLength(asset.description)}}</div>
          <div class="category-balance">{{parseFloat(asset.balance).toFixed(2)}}₽</div>
        </div>
        <div class="category">
          <div class="category-name category-add">&#65291;</div>
        </div>
      </div>
      <div class="category-type">Assets</div>
    </div>
    <div class="arrow">&#x203A;</div>
    <div class="category-block">
      <div class="expenses">
        <div v-for="expense in expenses" :key="expense.pk" class="category">
          <div class="category-name">{{limitWordLength(expense.description)}}</div>
          <div class="category-balance">{{parseFloat(expense.balance).toFixed(2)}}₽</div>
        </div>
        <div class="category">
          <div class="category-name category-add">&#65291;</div>
        </div>
      </div>
      <div class="category-type">Expenses</div>
    </div>
  </div>
</template>

<script>
import methods from "../methods.js";

export default {
  name: "Common",

  data() {
    return {
      incomes: null,
      assets: null,
      expenses: null,

      getURL: methods.getURL,
      getJSON: methods.getJSON,
      resetInitData: methods.resetInitData,
      limitWordLength: methods.limitWordLength
    };
  },

  beforeRouteEnter(to, from, next) {
    next(vm => vm.refreshData());
  },

  methods: {
    getCommonInfo() {
      this.getJSON(this.getURL("commonInfo")).then(data => {
        this.incomes = data.incomes;
        this.assets = data.assets;
        this.expenses = data.expenses;
      });
    },

    refreshData() {
      this.resetInitData();
      this.getCommonInfo();
    }
  }
};
</script>

<style scoped>
.common {
  display: flex;
  align-content: space-around;
  justify-content: center;

  /* filter: blur(3px); */
}

.category-block {
  display: flex;
  flex-direction: column;

  border: 0.5px dashed darkgray;
  border-radius: 5px;

  margin: 5px;
  align-content: space-between;
}
.category-type {
  font-weight: 300;
  font-size: 0.5rem;
  text-align: center;
}

.incomes,
.assets,
.expenses {
  display: flex;
  flex-direction: column;

  height: 100%;
}
.expenses {
  flex-direction: row;
  flex-wrap: wrap;

  align-content: flex-start;
  justify-content: safe center;
  max-width: 690px;
}

.arrow {
  font-size: 2rem;
  align-self: center;
}

.category {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;

  height: 80px;
  width: 80px;

  border: 0.5px solid darkgray;
  border-radius: 5px;

  margin: 3px;
  padding: 3px;
}
.category:hover {
  background: rgb(240, 240, 240);
}
.category:active {
  color: lightgray;
  background: rgb(72, 72, 72);
}

.category-add {
  display: block;
  line-height: 50px;

  font-size: 2rem !important;
  font-weight: 100 !important;
}

.category-name,
.category-balance {
  font-size: 0.7rem;
  text-align: center;

  margin: 2px;
  user-select: none;
}
.category-balance {
  font-weight: 400;
}
.category-name {
  font-weight: 500;
}
</style>
