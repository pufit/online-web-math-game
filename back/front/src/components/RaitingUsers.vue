<template>
  <div class="container">
    <div class="row">
      <table class="table table-hover">
        <thead>
        <tr>
          <th>#</th>
          <th>Username</th>
          <th>Лучший результат по количеству верных ответов</th>
          <th>Уровень сложности</th>
        </tr>
        </thead>
        <tbody>
          <tr v-for="(user, index) in listResultUsers">
            <td>{{ index + 1 }}</td>
            <td>{{ user.displayName}}</td>
            <td class="correct-answer"> {{ user.rate }}</td>
            <td> Сложный </td>
          </tr>
        </tbody>
      </table>
      <div v-if="showSpinner" class="spinner-wrapper">
        <img src="../assets/spinner.gif" alt="spinner">
      </div>
    </div>
  </div>
</template>


<script>
  import * as firebase from  'firebase'
  export  default {
    name: 'RaitingUsers',
    data() {
      return {
        listResultUsers: [{
          displayName: 'admin',
          rate: 3
        }],
        showSpinner: false
      }
    },
    created() {
    // this.getRaitingUsers();
    },
    methods: {
      getRaitingUsers() {
        firebase.database().ref('/TotalUsers').once('value').then((snapshot) => {
          this.getResultUser(snapshot.val());
        })
      },
      getResultUser(objectResultUser) {
        let _this = this;
        for (let key in objectResultUser) {
          _this.listResultUsers.push({
            'displayName': objectResultUser[key].displayName,
            'Rate': objectResultUser[key].resultTesting
          })
        }
        for (let i = 0; i < this.listResultUsers.length; i++) {
          for (let k = 0; k < this.listResultUsers.length; k++) {
            if (this.listResultUsers[i].Rate > this.listResultUsers[k].Rate) {
              [this.listResultUsers[i], this.listResultUsers[k]] = [this.listResultUsers[k], this.listResultUsers[i]]
            }
          }
        }
        this.showSpinner = false;
      }
    }
  }
</script>

<style scoped>

  .correct-aswer {
    color: green;
    font-weight: 900;
    font-size: 18px;
  }

  body {
    font-family: 'Open Sans', sans-serif;
  }

  .row {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
    grid-gap: 30px;

    min-height: 420px;
    text-align: center;

    border-radius: 10px;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
    border: 2px solid black;

    background: beige;
  }

  .raiting-table {
    margin-top: 30px;
  }
</style>
