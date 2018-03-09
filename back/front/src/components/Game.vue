<template>
  <main @keyup.13="sendAnswer">
    <div class="container">
      <article class="current-game">
          <section class="c-g__section_users_chat col-lg-12">
              <h2 class="text-center mb-3">Сведения об игре</h2>
              <section class="section-about-game">
                <div class="about-game__state-game">
                  <h3 class="about-game__title">Подключенные пользователи и их результат:</h3>
                  <div class="template-user text-danger">
                    <span>Evgen:</span>
                    <span class="text-success"> 5 points</span>
                    <span class="text-secondary">(lider lobby)</span>
                  </div>
                  <div class="template-user text-danger">
                    <span>Jenya:</span>
                    <span class="text-success">3 points</span>
                  </div>
                  <span class="text-secondary d-block">Всё происходит в реальном времени</span>
                  <div v-if="rightStartGame" class="control_btn_state_game">
                    <button class="btn btn_def btn_size"
                            v-if="testingComplete"
                            type="button"
                            id="btn-start"
                            @click="startTesting">Начать игру</button>

                    <button class="btn btn_def btn_size"
                            v-else type="button"
                            id="btn-end"
                            @click="finishGame">Прервать</button>
                  </div>
                  <div v-else-if="testingComplete & !rightStartGame" class="alert alert-success control_btn_state_game" role="alert">
                    Ожидайте,когда лидер лобби начнёт игру!
                  </div>
                </div>
                <dir-chat></dir-chat>
              </section>
            <div class="alert alert-primary" role="alert">
              Совет: Используйте клавиши клавиатуры,ввод значений осуществляется быстрей.
              Как только вы начнете играть - ваш фокус будет на вводимом поле,просто нажимайте цифры на клавиаутуре.
            </div>
            <hr>
          </section>
          <section class="col-lg-12">
            <div class="output_fields">
              <div class="output_fields__example">
                <time>Осталось времени: <span id="outputTime" v-if="!testingComplete"></span></time>
                <h1 class="display-4">- Пример -</h1>
              </div>
              <div v-if="testingComplete">
                <h4>Результат игры</h4>
                <h4>Правильных ответов: <span class="text-success">{{countCorrectAnswer}}</span></h4>
                <table class="table table-sm">
                  <thead>
                  <tr>
                    <th scope="col">Пример:</th>
                    <th scope="col">Ваш ответ:</th>
                    <th scope="col">Верный ответ:</th>
                  </tr>
                  </thead>
                  <tbody>
                  <tr v-for="result in listResultTest">
                    <td :class="result.userAnswer === result.Correct ? 'border_green' : 'border_red' ">{{result.Example}}</td>
                    <td :class="result.userAnswer === result.Correct ? 'border_green' : 'border_red' ">{{result.userAnswer}}</td>
                    <td :class="result.userAnswer === result.Correct ? 'border_green' : 'border_red' ">{{result.Correct}}</td>
                  </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </section>
        <section class="c-g__section-game col-lg-12">
          <input v-model="dataCurrentTesting.userAnswer" class="field_answer"
                 type="text"
                 placeholder="Здесь будет отображаться ваш вводимый ответ"
                 @input="checkTrueAnswer">
          <div class="section-game__numbers-field">
            <button type="button" class="btn btn-outline-info" @click="addNumber($event.target.value)" value="1">1</button>
            <button type="button" class="btn btn-outline-info" @click="addNumber($event.target.value)" value="2">2</button>
            <button type="button" class="btn btn-outline-info" @click="addNumber($event.target.value)" value="3">3</button>
            <button type="button" class="btn btn-outline-info" @click="addNumber($event.target.value)" value="4">4</button>
            <button type="button" class="btn btn-outline-info" @click="addNumber($event.target.value)" value="5">5</button>
            <button type="button" class="btn btn-outline-info" @click="addNumber($event.target.value)" value="6">6</button>
            <button type="button" class="btn btn-outline-info" @click="addNumber($event.target.value)" value="7">7</button>
            <button type="button" class="btn btn-outline-info" @click="addNumber($event.target.value)" value="8">8</button>
            <button type="button" class="btn btn-outline-info" @click="addNumber($event.target.value)" value="9">9</button>
            <button type="button" class="btn btn-outline-info" @click="addNumber($event.target.value)" value="0">0</button>
            <button type="button" class="btn btn-outline-info" @click="addNumber($event.target.value)" value="-">-</button>
            <button type="button" class="btn btn-outline-info" @click="addNumber($event.target.value)" value=".">.</button>
            <button type="button" class="btn btn-large btn-danger" @click="sendAnswer">Отправить результат</button>
            <button type="button" class="btn btn-large btn-danger" @click="removeAnswer">Очистить</button>
          </div>
        </section>
      </article>
    </div>
  </main>
</template>


<script>

  export default  {
    name: 'StartGame',
    data () {
      return {
        socket: null,
        rightStartGame: false,

        textBanner: 'Привет! Подожди начала игры!',

        testingComplete: true,
        listResultTest: [],
        countCorrectAnswer: 0,
        timeCycle: '',
        timeCycle2: '',

        mathOperation: ['+', '-', '*', '/'],
        objectGameSettings: {
          rangeNumber: [10, 50],
          rangeNumber1: [1, 20]
        },
        dataCurrentTesting: {
          currentExample: '',
          correctAnswer: '',
          userAnswer: ''
        }
      }
    },
    created() {
      // if (!this.$store.state.participantGame) this.$router.push({name: 'Lobby'});
      this.socket = this.$store.state.socket;
      this.callAnimationBanner();
      window.addEventListener('blur', this.lossFocusDuringGame);
    },
    beforeDestroy() {
      this.$store.commit('setParticipantGame', false);
    },
    methods: {
      callAnimationBanner() {
        this.$store.commit('setAnimation', {
          run: true,
          textBanner: this.textBanner
        });
        this.textBanner = 'Раунд окончен'
      },
      generateExample(min, max) {
        return Math.round(min - 0.5 + Math.random() * (max - min + 1));
      },
      getNumber(range1, range2) {
        let number1 = this.generateExample(range1, range2);
        let number2 = this.generateExample(range1, range2);
        return [number1, number2]
      },
      checkTrueAnswer() {
        this.dataCurrentTesting.userAnswer = this.dataCurrentTesting.userAnswer.replace(/[^-.0-9]/ig, '');
        if (parseInt(this.dataCurrentTesting.userAnswer, 10) === this.dataCurrentTesting.correctAnswer) this.sendAnswer();
      },
      startTesting() {
        this.listResultTest = [];
        this.countCorrectAnswer = 0;
        this.testingComplete = false;
        this.$store.commit('setStateGame', true);

        let timeForCurrentTesting = 10;
        let totalTestingTime = 10;

        document.querySelector('.field_answer').focus();
        this.updateCurrentExample();

        // ненадежные циклы
        setTimeout(() => {
          document.querySelector('#outputTime').innerText = timeForCurrentTesting--;
        }, 0);
        this.timeCycle = setInterval(() => {
          if (document.querySelector('#outputTime')) document.querySelector('#outputTime').innerText = timeForCurrentTesting--;
        }, 1000);

        this.timeCycle2 = setTimeout(this.finishGame, totalTestingTime * 1000);
      },
      updateCurrentExample() {
        let indexMathOperation = this.generateExample(0, 3);
        let mathOperation = this.mathOperation[indexMathOperation];

        if (mathOperation === '+') {
          let [number1, number2] = this.getNumber(this.objectGameSettings.rangeNumber[0], this.objectGameSettings.rangeNumber[1]);
          this.dataCurrentTesting.correctAnswer = number1 + number2;
          this.dataCurrentTesting.currentExample = `${number1} + ${number2}`
        } else if (mathOperation === '-') {
          let [number1, number2] = this.getNumber(this.objectGameSettings.rangeNumber[0], this.objectGameSettings.rangeNumber[1]);
          this.dataCurrentTesting.correctAnswer = number1 - number2;
          this.dataCurrentTesting.currentExample = `${number1} - ${number2}`
        } else if (mathOperation === '*') {
          let [number1, number2] = this.getNumber(this.objectGameSettings.rangeNumber1[0], this.objectGameSettings.rangeNumber1[1]);
          this.dataCurrentTesting.correctAnswer = number1 * number2;
          this.dataCurrentTesting.currentExample = `${number1} * ${number2}`
        } else if (mathOperation === '/') {
          let [number1, number2] = this.getNumber(this.objectGameSettings.rangeNumber1[0], this.objectGameSettings.rangeNumber1[1]);

          while ((number1 / number2).toString().length > 2) {
            [number1, number2] = this.getNumber(this.objectGameSettings.rangeNumber[0], this.objectGameSettings.rangeNumber[1]);
          }

          this.dataCurrentTesting.correctAnswer = number1 / number2;
          this.dataCurrentTesting.currentExample = `${number1} / ${number2}`
        }

        if (document.querySelector('.display-4')) document.querySelector('.display-4').innerText = this.dataCurrentTesting.currentExample;
      },
      finishGame() {
        clearInterval(this.timeCycle);
        clearTimeout(this.timeCycle2);
        this.testingComplete = true;
        this.$store.commit('setStateGame', false);
        this.updateUsedFields();
        this.callAnimationBanner();
      },
      updateUsedFields() {
        if (document.querySelector('#outputTime')) document.querySelector('#outputTime').innerText = '';
        if (document.querySelector('.display-4')) document.querySelector('.display-4').innerText = '- Пример -';
        this.dataCurrentTesting.userAnswer = '';
      },
      sendAnswer() {
        if (this.dataCurrentTesting.userAnswer.length === 0) return;
        if (!this.testingComplete) {
          if (parseInt(this.dataCurrentTesting.userAnswer, 10) === this.dataCurrentTesting.correctAnswer) this.countCorrectAnswer++;
          this.listResultTest.push({
            'Example': this.dataCurrentTesting.currentExample,
            'Correct': this.dataCurrentTesting.correctAnswer,
            'userAnswer': parseInt(this.dataCurrentTesting.userAnswer, 10)
          });
          this.updateCurrentExample();
        }
        this.dataCurrentTesting.userAnswer = '';
      },
      addNumber(value) {
        this.dataCurrentTesting.userAnswer += value;
        this.checkTrueAnswer();
      },
      removeAnswer() {
        this.dataCurrentTesting.userAnswer = '';
      },
      lossFocusDuringGame() {
        if (!this.testingComplete) this.updateCurrentExample();
      },
    }
  }




</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>


  .border_green {
    border: 2px solid green;
  }

  .border_red {
    border: 2px solid crimson;
  }

  main {
    position: relative;
    display: grid;
    grid-template-rows: 1fr;
    grid-template-columns: 1fr;
  }


  .current-game {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 0.5fr minmax(1fr, 5fr) 1fr;
    grid-gap: 20px;

    min-height: 550px;

    border-radius: 10px;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
    border: 2px solid black;

    background: beige;
  }

  .section-about-game {
    display: grid;
    grid-template-columns: 1fr 1.2fr;
    grid-template-rows: 1fr;
    grid-gap: 90px;

    margin-bottom: 10px;
  }

  .about-game__state-game {
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;

  }

  .about-game__title {
    font-size: 24px;
  }

  .template-user {
    margin-left: 5px;
    font-weight: 600;
    font-size: 20px;
  }

  .btn_size {
    width: 80%;
    min-height: 35px;
  }

  .control_btn_state_game {
    display: flex;
    justify-content: center;


    margin-bottom: 10px;
    margin-top: auto;

    text-align: center;
  }

  .output_fields {
    display: grid;
    grid-template-columns: 2fr 3fr;

    text-align: center;
  }

  .output_fields__example {
    margin-right: 5px;
    border-right: 1px solid black;
  }

  .c-g__section-game {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    padding: 20px;

    border-radius: 10px;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
    border: 2px solid black;
  }

  .section-game__numbers-field {
    display: grid;
    grid-template-columns: 15fr 15fr 15fr;
    grid-template-rows: 35px 35px 35px;
    grid-gap: 5px;

    width: 65%;
    padding: 10px;

    border: 2px solid teal;
    border-radius: 5px;
  }

  .field_answer {
    width: 65%;
    margin-bottom: 20px;
    min-height: 40px;
    padding: 0 10px;

    border: 1px solid #cccccc;
    border-radius: 3px;
  }

  .field_answer:focus {
    -webkit-box-shadow: 0px 0px 5px #007eff;
    moz-box-shadow: 0px 0px 5px #007eff;
    box-shadow: 0px 0px 5px #007eff;
  }

</style>
