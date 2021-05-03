
export let dataHandler = {
    _data: {}, // it is a "cache for all data received: boards, cards and statuses. It is not accessed from outside.
    _api_get: function (url, callback) {
        // loads data from API, parses it and calls the callback with it
        fetch(url, {
            method: 'GET',
            credentials: 'same-origin'
        })
        .then(response => response.json())  // parse the response as JSON
        .then(json_response => callback(json_response));  // Call the `callback` with the returned object
    },
    _api_post: function (url, data, callback) {
        fetch(url, {
            method: 'POST',
            credentials: 'include',
            body: JSON.stringify(data),
            cache: "no-cache",
            headers: new Headers({
                "content-type": "application/json"
            })
        })
        .then(response => response.json())  // parse the response as JSON
        .then(json_response => callback(json_response));  // Call the `callback` with the returned object
    },
    init: function () {
    },
    getBoards: function (callback) {

        this._api_get('/get-boards', (response) => {
            this._data['boards'] = response;
            callback(response);
        });
    },
    getBoard: function (boardId, callback) {
        this._api_get("/get-board/"+boardId+"", (response) => {
             this._data['board'] = response;
             callback(response);
        });
    },
    getStatuses: function (boardId, callback) {
        this._api_get("/get-statuses/"+boardId+"", (response) => {
             this._data['statuses'] = response;
             callback(response);
        });
    },
    getStatus: function (statusId, callback) {
    },

    getCardsByBoardId: function (boardId, callback) {

        this._api_get("/get-cards/"+boardId+"", (response) => {
             this._data['cards'] = response;
             callback(response);
        });
    },
    getCard: function (cardId, callback) {
    },
    createNewBoard: function (boardTitle, boardType, callback) {
        this._api_get("/save-board/"+boardTitle+"/"+boardType+"", () => {
             callback();

        });

        // creates new board, saves it and calls the callback function with its data
    },
    createNewCard: function (cardTitle, boardId, callback) {
        this._api_get("/save-card/"+boardId+"/"+cardTitle+"", () => {
            callback();
        });
        // creates new card, saves it and calls the callback function with its data
    },
    changeBoardName: function (boardId, newName, callback){
        this._api_get("/change-title/"+boardId+"/"+newName+"", () => {
            callback();

        });
    },

    changeCardTitleName: function (newName, card_id, callback){
        this._api_get("/change-card-title/"+card_id+"/"+newName+"", () => {
            callback();
        });
    },

    changeColumnTitleName: function (columnName, column_id, board_id, callback){
        this._api_get("/change-column-title/"+columnName+"/"+column_id+"/"+board_id+"", () => {
            callback();
        });
    },

    changeCardOrder: function (boardId, cardsId, callback) {
       this._api_get("/change-card-order/"+boardId+'/'+cardsId, () => {
          callback();
       });
    },


    deleteBoard: function (boardId, callback){
        this._api_get("/delete-board/"+boardId, () => {
            callback();
        })
    },


    deleteCard: function (boardId, cardId, callback){
        this._api_get("/delete-card/"+boardId+'/'+cardId, () => {
            callback();
        })
    },

    checkUserInputAndRegisterOrLogin: function (userData, currentMode, callback) {

        this._api_post('/account', [userData, currentMode], (response) => {
          callback(response);
       });
    },

    logoutUser: function (callback) {
        this._api_get("/logout", () => {
            callback();
        })
    },

    archiveCard: function(cardId, boardId, archive, callback) {
        this._api_get('/archive-card/'+cardId+'/'+boardId+'/'+archive, ()=> {
            callback();
        })
    },

    deleteStatus: function (boardId, statusId, callback) {
         this._api_get('/delete-status/'+boardId+'/'+statusId, ()=> {
            callback();
        })
    }

};
