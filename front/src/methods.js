export default {
  name: "methods",

  /**
   * Function make URL request and parse JSON answer
   * @param url, string
   * @param params, fetch {Object}
   * @return {Promise}, fetch promise
   */
  getJSON(url, params = {}) {
    return fetch(url, params)
      .then(response => response.json())
      // eslint-disable-next-line no-console
      .catch(error => console.log(error))
  },

  /**
   * URL API logic: return URL string by input params.
   * @param name, {string} - action name
   * @param param, {string} - param is container ID
   * @return url, {string}
   */
  getURL(name, param = null) {
    switch (name) {
      case "commonInfo":
        return "/api/common-info/";

      case "createAsset":
        return "/api/assets/";
      case "detailAsset":
        return `/api/assets/${param}/`;
      case "incomingAsset":
        return `/api/assets/${param}/incoming/`;
      case "outgoingAsset":
        return `/api/assets/${param}/outgoing/`;

      case "createIncome":
        return "/api/incomes/";
      case "detailIncome":
        return `/api/incomes/${param}/`;

      case "createExpense":
        return "/api/expenses/";
      case "detailExpense":
        return `/api/expenses/${param}/`;
      case "incomingExpense":
        return `/api/expenses/${param}/incoming/`;

      case "createIncomeTransaction":
        return "/api/income-transactions/";
      case "detailIncomeTransaction":
        return `/api/income-transactions/${param}/`;

      case "createExpenseTransaction":
        return "/api/expense-transactions/";
      case "detailExpenseTransaction":
        return `/api/expense-transactions/${param}/`;

      case "createUser":
        return "/rest-auth/registration/";
      case "showUser":
        return "/rest-auth/user/";
      case "loginUser":
        return "/rest-auth/login/";
      case "logoutUser":
        return "/rest-auth/logout/";
    }
  },

  /**
   * Function parse Cookie header and get value by name
   * @param {string}, cookie key name
   * @return {string}, cookie value
   */
  getCookie(key) {
    const regexp = new RegExp(`${key}=([^;]+)`);
    const value = regexp.exec(document.cookie);

    if (value === null) {
      return '';
    }
    return value[1];
  },

  /**
   * Function reset data values
   */
  resetInitData() {
    Object.assign(this.$data, this.$options.data.apply(this));
  },

  /**
   * Function slice each word in string.
   * @param inputString, {string} - input string
   * @param wordLimit, {integer} - word length limit
   */
  limitWordLength(inputString, wordLimit = 9) {
    let words = inputString.split(/\s+/);
    const res = words
      .map(w =>
        w.length >= wordLimit + 1 ? `${w.slice(0, wordLimit)}\u2026` : w
      )
      .join(" ");
    return res;
  }
};