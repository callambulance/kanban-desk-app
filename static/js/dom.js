// It uses data_handler.js to visualize elements
import { dataHandler } from "./data_handler.js";

let thisTable
let boardNames = []
// let divTable = document.getElementById('div_table');
let newBoardButton = document.getElementById("new_board");
let newBoardInputName = document.getElementById('new_board_input');
let newBoardDiv = document.getElementById('new_board_div');
let saveButton = document.getElementById("new_board_save");
let buttonId;
// let boardTitle = document.getElementById("board_title");

const registerBtn = document.getElementById('register-btn');
const loginBtn = document.getElementById('login-btn');
const logoutBtn = document.getElementById('logout-btn');
const accountPopup = document.getElementById('account-popup');
const newPrivateBoardBtn = document.getElementById('new_private_board');

const usernameInput = document.getElementById("username");
const pwdInput = document.getElementById('password');
const submitBtn = document.getElementById('submit-btn');
const errorMsg = document.getElementById('error-msg');
const confirmMsg = document.getElementById('confirmation-msg');
const welcomeUser = document.getElementById('welcome-user');

const registrationMode = "registration";
const loginMode = "login";
const logoutMode = "logout";
let currentMode = "";
const ordinaryType = "ordinary";
const privateType = "private";
let newBoardType = ordinaryType;

let session_username = "";


export let dom = {

    init: function () {
        newBoardButton.addEventListener('click', function() {
            newBoardType = ordinaryType;
            dom.newBoardInput();
        });
        newPrivateBoardBtn.addEventListener('click', function() {
            newBoardType = privateType;
            dom.newBoardInput();
        });
        saveButton.addEventListener('click', this.SaveNewBoard);
        registerBtn.addEventListener('click', function() {
            currentMode = registrationMode;
            dom.fillPopup();
        });
        loginBtn.addEventListener('click', function() {
            currentMode = loginMode;
            dom.fillPopup();
        });
        logoutBtn.addEventListener('click', function() {
            currentMode = logoutMode;
            dataHandler.logoutUser(dom.logout);
        });
        submitBtn.addEventListener('click', this.validateInput);

        // This function should run once, when the page is loaded.
    },
    loadBoards: function () {

        // retrieves boards and makes showBoards called
        dataHandler.getBoards(function(boards){
            dom.showBoards(boards);
        });
    },

    showBoards: function (boards) {
        // shows boards appending them to #boards div
        let boardList = '';

        if (boards.length === 2 && Array.isArray(boards[0])) {
            let ordinaryBoards = boards[0];
            let privateBoards = boards[1];

            // for (let board of privateBoards) {
            //     board['id'] += '-p';
            // }
            boards = privateBoards.concat(ordinaryBoards);
        }


        //adding every board
        for(let board of boards) {
                boardList += `
                <li contenteditable id="save_title_${board.id}" class="board_title">${board.title}</li>
               
                <button type="button" id="title_${board.id}" class="save_name">Save name</button>
          
                <button type="button" id="${board.id}" class="table-button" >Show board</button>
                <button style="display: none" type="button" id="hide${board.id}" class="table-button-hide" >Hide board</button>
                <button type="button" class="delete-btn" style="background: transparent" id="delete-board${board.id}"><i class="fa fa-trash-o"></i></button>

                <div id="t${board.id}" class="board" style="display: none"></div>
                
                
            `;
            boardNames.push(board.title)
        }


        const outerHtml = `
            <ul class="board-container">
                ${boardList}
            </ul>
        `;


        let boardsContainer = document.querySelector('#boards');
        boardsContainer.insertAdjacentHTML("beforeend", outerHtml);

        // console.log(document.querySelectorAll('.delete-btn'))
        document.querySelectorAll('.delete-btn').forEach(item =>{
            // console.log(item)
            item.addEventListener('click', event=>{
                if (confirm("Are you sure you want to delete this board?")) {
                    dataHandler.deleteBoard(item.id, function () {
                        let boardContainer = document.querySelector('.board-container');
                        boardContainer.parentNode.removeChild(boardContainer);
                        dom.loadBoards();
                        console.log("board deleted");
                    })
                }
            })
        })

        //adding event listener to every button for showing the board
        document.querySelectorAll('.table-button-hide').forEach(item =>{
            item.addEventListener('click', event => {
                buttonId = item.id.replace('hide', '')
                let boardToHide = document.getElementById('t'+ buttonId)
                let buttonToHide = document.getElementById('hide' + buttonId)
                boardToHide.style.display = 'none';
                buttonToHide.style.display = 'none';
                })
        })

        document.querySelectorAll('.table-button').forEach(item =>{
            item.addEventListener('click', event => {
                buttonId = item.id
                // console.log(buttonId)
                this.loadCards(item.id)
                })
        })

        //adding events to save new board title
        document.querySelectorAll('.save_name').forEach(item =>{
            item.addEventListener('click', event=>{
                let newName = document.getElementById('save_'+item.id).innerHTML
                console.log(newName)
                let board_id = item.id.replace(/\D/g, '');
                console.log(board_id)
                dom.SaveNewBoardTitle(board_id, newName)


            })
        })

    },

    SaveNewBoardTitle: function (board_id, newName){
        dataHandler.changeBoardName(board_id, newName, function(){
            //remove everything from the board container so all boards will be shown in one <ul>
            let boardContainer = document.querySelector('.board-container')
            boardContainer.parentNode.removeChild(boardContainer)
            dom.loadBoards(dom.loadCards(buttonId));
        });


    },

    // retrieves cards and makes showCards called
    loadCards: function (boardId){
        dataHandler.getCardsByBoardId(boardId,function(cards) {
            dataHandler.getStatuses(boardId, function (statuses){
                dataHandler.getBoard(boardId, function (board) {
                    dom.showCards(boardId, cards, statuses, board)
                })
            })
        })
    },

    showCards: function (boardId, cards, statuses, board) {
        // let count = 0
        //checking if there is any cards for this board
            let headersList = '';
            let tablesListArchive = '';
            //sorting cards
            for (let status of statuses) {
                let statusesList = [];
                let tablesList = '';
                for (let card of cards) {

                    if (status.title == card.status_title) {
                        if (card.archived == "0") {
                            tablesList += `
                                 <div draggable="true"  class="card card${boardId}" id="card${card.id}" order="${card.card_order}" >
                                    <div class="card-title" id="card_title${card.id}" contenteditable>${card.card_title}</div>
                                    <button type="button" class="delete-btn${board.id}" style="background: transparent" id="delete-card${card.id}"><i class="fa fa-trash-o"></i></button>
                                    <button type="button" class="archive-button${board.id}" style="background: transparent" id="archive-card${card.id}"><i class="fas fa-save"></i></button>
                                 </div>
                            `;
                        } else {
                            tablesListArchive += `
                                     <div class="card">
                                        <div class="card-title" contenteditable>${card.card_title}</div>
                                        <button type="button" class="unarchive-button${board.id}" style="background: transparent" id="unarchive-card${card.id}"><i class="fas fa-undo"></i></button>
                                     </div>
                                `

                        }
                    }
                }


                    //adding board to the div
                    headersList += `
                        <div class="board-column" id="${status.id}">
                            <div class="board-header" id ="board-${board.id}">
                            <div contenteditable id="column${status.id}" class="board-column-title">${status.title}</div>
                            <button type="button" class="delete-status-${board.id}" style="background: transparent" id="delete-${status.id}"><i style="color: black" class="fa fa-trash-o"></i>>button</button>
                            </div>
                            <div class="board-column-content">
                            ${tablesList}
                            </div>
                        </div> 
                    `



            //adding board to the div
            let outerHTML = `
                                <h2 class="board-title"  >${board.title}</h2>
                                <br>
                                <input id="new-card${board.id}">
                                <button type="button" id="new-card-button${board.id}">Create new card</button>
                                <div class="board-columns board-columnss${boardId}">
                                    ${headersList}
                                </div>
                         `

            if (tablesListArchive.length != 0) {
                outerHTML += `
                        <button type="button" class="archived-button" id="a${boardId}">Archived Cards</button>
                        <button style="display: none" type="button" class="archived-button-hide" id="aH${boardId}">Hide Archived Cards</button>
                        <div style="display: none" class="board-columns" id="at${boardId}">
                                ${tablesListArchive}
                        </div>
                        `



                document.addEventListener('click', function (e) {
                    if(e.target && e.target.id == 'a'+boardId ){
                        let buttonClickedId = boardId;
                        let archivedTable = document.getElementById("at" + buttonClickedId)
                        let hideButton = document.getElementById('aH' + buttonClickedId)
                        hideButton.style.display = 'inline'
                        archivedTable.style.display = 'flex'
                    }
                })

                document.addEventListener('click', function (e){
                    if(e.target && e.target.id == 'aH'+boardId) {
                        let hideButtonId = boardId
                        let hideButton = document.getElementById('aH'+hideButtonId)
                        let archivedTable = document.getElementById('at'+hideButtonId)
                        hideButton.style.display = 'none'
                        archivedTable.style.display = 'none'
                    }
                })

            }

            //adding table to the page
            thisTable = document.getElementById("t" + boardId)
            thisTable.innerHTML = '';
            thisTable.insertAdjacentHTML("beforeend", outerHTML);
            let hideButton = document.getElementById('hide' + boardId)
            hideButton.style.display = 'inline';

            document.querySelectorAll('.card-title').forEach(item => {
                let cardName = item.innerHTML;
                let card_id = item.id.replace(/\D/g, '');
                item.addEventListener('keydown', event => {
                    if (event.keyCode == 13) {
                        event.preventDefault();
                        cardName = item.innerHTML;
                        // let newTitleName = item.innerHTML
                        item.blur();
                        dom.changeCardTitleName(cardName, card_id)
                    } else {
                        document.body.addEventListener('click', (ev) => {
                            item.innerHTML = cardName;
                        }, {once: true});
                    }
                })
            })

            let newCardBtn = document.getElementById('new-card-button' + board.id);
            newCardBtn.addEventListener('click', event => {
                this.addNewCard(board.id)
            })



                  document.querySelectorAll('.delete-status-'+board.id).forEach(item =>{
                    item.addEventListener('click', event=>{
                        if (confirm("Are you sure you want to delete?")) {
                            let statusId = item.id.replace(/\D/g, '');
                            console.log(statusId, boardId)
                            dataHandler.deleteStatus(boardId, statusId, function (){
                                dom.loadCards(boardId)
                            })
                        }
                    })
                })

                document.querySelectorAll('.delete-button'+boardId).forEach(item =>{
                    item.addEventListener('click', event=>{
                        if (confirm("Are you sure you want to delete?")) {
                            dataHandler.deleteCard(boardId, item.id, function () {
                                dom.loadCards(boardId)
                            })
                        }
                    })
                })

            document.querySelectorAll('.archive-button'+boardId).forEach(item =>{
                item.addEventListener('click', event=>{
                    dataHandler.archiveCard(item.id, boardId, 1, function (){
                        dom.loadCards(boardId)
                    })
                })
            })

            document.querySelectorAll('.board-column-title').forEach(item => {
                let columnName = item.innerHTML;
                let column_id = item.id.replace(/\D/g, '');

                item.addEventListener('keydown', event => {
                    if (event.keyCode == 13) {
                        event.preventDefault();
                        columnName = item.innerHTML;
                        let board_id = document.getElementById(item.id).parentElement;
                        board_id = board_id.id.slice(6);
                        // console.log(board_id +" this!!")
                        // if (count === 0){
                            dom.changeColumnTitleName(columnName, column_id, board_id)
                            // count+=1


                    } else {
                        document.body.addEventListener('click', (ev) => {
                            item.innerHTML = columnName;
                        }, {once: true});
                    }
                }) ;
            })
            document.querySelectorAll('.unarchive-button'+boardId).forEach(item =>{
                item.addEventListener('click', event=>{
                    dataHandler.archiveCard(item.id, boardId, 0, function (){
                        dom.loadCards(boardId)
                    })
                })
            })


            dom.cardsToggle(thisTable);
            dom.initDragAndDrop(boardId);
        }
    },


    changeColumnTitleName: function (columnName, column_id, board_id){
        // console.log(board_id)
        dataHandler.changeColumnTitleName(columnName, column_id, board_id, function (){
            dom.loadCards(board_id)
        })

    },

    changeCardTitleName: function (newCardTitleName, card_id){
        dataHandler.changeCardTitleName(newCardTitleName, card_id)

    },

    // showing and hiding board
    cardsToggle: function (thisTable) {
            if (thisTable.style.display === "none") {
                thisTable.style.display = "block";
            }
            // else{
            //     thisTable.style.display = "none";
            //     thisTable.innerHTML = '';
            // }
            },

    newBoardInput: function () {
        if (newBoardDiv.style.display === "none") {
            newBoardDiv.style.display = "block"
        } else {
            newBoardDiv.style.display = "none"
            newBoardInputName.value = ""
        }

        },

    SaveNewBoard: function () {
            //saving value of the new board name
            let newBoardName = newBoardInputName.value;
            dom.newBoardInput()

        //saving the name
        dataHandler.createNewBoard(newBoardName, newBoardType, function(){
            //remove everything from the board container so all boards will be shown in one <ul>
            let boardContainer = document.querySelector('.board-container')
            boardContainer.parentNode.removeChild(boardContainer)
            dom.loadBoards();
        });
    },

    addNewCard: function(boardId) {
        let newCardName = document.getElementById('new-card'+boardId).value;

        dataHandler.createNewCard(newCardName, boardId, function () {
            dom.loadCards(boardId)
        });
    },

    initDragAndDrop: function (boardId) {
        const draggables = document.querySelectorAll('.card'+boardId)
        const containers = document.querySelectorAll('.board-column-content')
        draggables.forEach(draggable => {
          draggable.addEventListener('dragstart', () => {
            draggable.classList.add('drag-sort-active')
          })

          draggable.addEventListener('dragend', () => {
            draggable.classList.remove('drag-sort-active')
              let cardId = [];
              for (const board of document.getElementsByClassName('board-columnss'+boardId)[0].getElementsByClassName('board-column')) {
                  let columnsNumber = board.id
                  for (const card of board.getElementsByClassName('card'+boardId)) {
                      cardId.push(columnsNumber+card.id)
                  }
              }

              dataHandler.changeCardOrder(boardId, cardId, function () {

              });

          })
        })

        containers.forEach(container => {
          container.addEventListener('dragover', e => {
            e.preventDefault()
            const afterElement = getDragAfterElement(container, e.clientY)
            const draggable = document.querySelector('.drag-sort-active')
            if (afterElement === null) {
              container.appendChild(draggable)
            } else {
              container.insertBefore(draggable, afterElement)
            }
          })
        })

        function getDragAfterElement(container, y) {
          const draggableElements = [...container.querySelectorAll('.card:not(.drag-sort-active)')]

          return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect()
            const offset = y - box.top - box.height / 2
            if (offset < 0 && offset > closest.offset) {
              return { offset: offset, element: child }
            } else {
              return closest
            }
          }, { offset: Number.NEGATIVE_INFINITY }).element
        }
    },

    displayMsg: function (element, text) {
        element.style.display = 'block';
        element.innerText = text;
    },

    fillPopup: function () {
        const header = document.getElementById('popup-header')

        usernameInput.placeholder = "Enter username";
        pwdInput.placeholder = "Password";
        usernameInput.value = "";
        pwdInput.value = "";

        errorMsg.style.display = 'none';
        confirmMsg.style.display = 'none';

        if (currentMode == registrationMode) {
            header.innerText = "Registration";
        } else if (currentMode == loginMode) {
            header.innerText = "Login";
        }

        accountPopup.style.display = "block";
    },

    validateInput: function (evt) {
        session_username = usernameInput.value;
        let pwd = pwdInput.value;

        const userData = {
            username: session_username,
            password: pwd
        }

        evt.preventDefault();

        if (session_username == "" || pwd == "" || session_username == null || pwd == null) {
            dom.displayMsg(errorMsg, "Please, fill in both fields.");
        } else if (pwd.length < 6) {
            dom.displayMsg(errorMsg, "Password must be at least 6 characters long.");
        } else {
            dataHandler.checkUserInputAndRegisterOrLogin(userData, currentMode, dom.handleAPIUserResponse);
        }
    },

    handleAPIUserResponse: function (response) {
        // console.log(response, currentMode)
        if (currentMode===registrationMode && response===true) {
            currentMode = loginMode;
            dom.fillPopup();
            dom.displayMsg(confirmMsg, "You've been registered. Log in now.");
        } else if (currentMode===registrationMode && response===false) {
            dom.displayMsg(errorMsg, "This username is already taken. Please, choose another one.");
        } else if (currentMode===loginMode && response===true) {
            dom.fillPopup();
            accountPopup.style.display = "none";
            dom.login();
        } else if (currentMode===loginMode && response===false) {
            dom.displayMsg(errorMsg, "Invalid username or password. Please try again.");
        }
    },

    login: function () {
        let boardContainer = document.querySelector('.board-container')
        boardContainer.parentNode.removeChild(boardContainer)
        dom.loadBoards();
        welcomeUser.innerText += session_username.charAt(0).toUpperCase() + session_username.slice(1);
        welcomeUser.style.display = "block";
        loginBtn.style.display = "none";
        registerBtn.style.display = "none";
        logoutBtn.style.display = "block";
        newPrivateBoardBtn.style.display = "block";
    },

    logout: function () {
        let boardContainer = document.querySelector('.board-container')
        boardContainer.parentNode.removeChild(boardContainer)
        dom.loadBoards();
        welcomeUser.innerText = "You are logged in as ";
        welcomeUser.style.display = "none";
        loginBtn.style.display = "inline";
        registerBtn.style.display = "inline";
        logoutBtn.style.display = "none";
        newPrivateBoardBtn.style.display = "none";
        session_username = "";
    }

};
