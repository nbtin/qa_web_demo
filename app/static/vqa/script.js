/* Get element by its id to be able to interact with */
// const fileInput = document.getElementById('file-input');

const questionInput = document.getElementById('question-input');
const submitButton = document.getElementById('submit-button');


const textButton = document.querySelector("#text-button");
const imageButton = document.querySelector("#image-button");
const textInput = document.querySelector("#text-input");
const imageInput = document.querySelector("#image-input");
const answerBox = document.querySelector("#answer");

textButton.addEventListener("click", showTextInput);
imageButton.addEventListener("click", showImageInput);

const fileInput = document.createElement("input");
let is_text = true;

function reloadPage(){
    /* Re-load the page if user click on the 'location' */
    location.reload();
}

// fileInput.addEventListener('change', () => {
//     /* Change the image element with respect to the image was uploaded by user */
//     const file = fileInput.files[0];
//     if (file) {
//         const reader = new FileReader();
//         reader.addEventListener('load', () => {
//             imageElement.src = reader.result;
//         });
//         reader.readAsDataURL(file);
//     }
// });

submitButton.addEventListener('click', (event) => {



    


    /* Use fetch API to get the answer from user via API named '/answer' */
    event.preventDefault();

    // if(fileInput.files === null){
    //     console.log("1");
    // }
    // else{

    // const file = fileInput.files[0];
    const question = questionInput.value;
    // }
    answerBox.innerText = "Wait a second...";

    if (question) { // check if the file is uploaded and the question box is not empty
        // const formData = new FormData();
        // formData.append('image', file);
        // formData.append('questions', question);
        let input = {};
        console.log(is_text)
        if(is_text){
                input = {
                    context: textInput.value,
                    questions: questionInput.value,
                    is_image: false
                }
            console.log(1)

        }
        else {
            input = {
                context: imageInput.src,
                questions: questionInput.value,
                is_image: true
            }
            console.log(2);
        }
        fetch('answer/', {
        method: 'POST',
        body: JSON.stringify(input),
        headers: {
            'Content-Type': 'application/json'
        }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const likeButton = document.createElement('button');
                likeButton.innerHTML = 'Like';
                const dislikeButton = document.createElement('button');
                dislikeButton.innerHTML = 'Dislike';

                answerBox.appendChild(likeButton);
                answerBox.appendChild(dislikeButton);


                likeButton.addEventListener('click', () => {
                    // Handle like feedback here
                });
                
                dislikeButton.addEventListener('click', () => {
                    // Handle dislike feedback here
                });


                let result = data.data;
                console.log(result);
                const lines = result.split("\n");
                console.log(lines);
                
                if (lines.length > 1) {
                  for (let i = 0; i < lines.length; i += 3) {
                    let line_changed = '<b>' + lines[i] + '</b>';
                    if (i != 0) lines[i] = '<br>' + line_changed;
                    lines[i] = line_changed;
                
                    // Add like and dislike buttons
                    // let likeButton = '<button class="like-button" data-index="' + i + '">Like</button>';
                    // let dislikeButton = '<button class="dislike-button" data-index="' + i + '">Dislike</button>';
                    
                    if(i<lines.length - 1){
                        let likeButton = '<i class="fa fa-thumbs-up feedback_button" ></i>'
                        let dislikeButton = '<i class="fa fa-thumbs-down feedback_button"></i>'                
                        lines[i+1 ] += '   ' + likeButton + ' ' + dislikeButton;
                        }
                  }
                  result = lines.join("<br>");
                  console.log(result);
                }
                else{
                    // let likeButton = '<button class="like-button" data-index="' + 0 + '">Like</button>';
                    // let dislikeButton = '<button class="dislike-button" data-index="' + 0 + '">Dislike</button>';
                    let likeButton = '<i class="fa fa-thumbs-up feedback_button" ></i>'
                    let dislikeButton = '<i class="fa fa-thumbs-down feedback_button"></i>'
                    lines[0] += '   ' + likeButton + ' ' + dislikeButton;
                    result = lines[0]
                }
                
                answerBox.innerHTML = result;


                var feedbackFn = function() {
                console.log("clicked");
                var maxHeight = $(window).height() - 200;
                    var maxWidth = $(window).width() - 200;
                    const popupCard = $('<div>').addClass('popup-card');
                    const closeButton = $('<button>').text('X');
                    const answerTitle = $('<h2>').text('Thank you');
                    const answerText = $('<p>').text("Your feedback is valuable to us !");
            
                    closeButton.click(() => {
                        popupCard.remove();
                    });
                    popupCard.append(closeButton);
                    popupCard.append(answerTitle);
                    popupCard.append(answerText);
                    $('body').append(popupCard);
            
                    // Adjust the size of the popup card if necessary
                    const popupCardHeight = popupCard.height();
                    const popupCardWidth = popupCard.width();
            
                    if (popupCardHeight > maxHeight) {
                        popupCard.height(maxHeight);
                        popupCard.width(maxHeight * popupCardWidth / popupCardHeight);
                    }
            
                    if (popupCardWidth > maxWidth) {
                        popupCard.width(maxWidth);
                        popupCard.height(maxWidth * popupCardHeight / popupCardWidth);
                    }
};
const feedbackButtons = document.getElementsByClassName('feedback_button');

for (var i = 0; i < feedbackButtons.length; i++) {
    feedbackButtons[i].addEventListener('click', feedbackFn, false);
}
                
            } else {
                console.log(data);
                throw new Error('Error getting answer from server.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    else {
        answerBox.innerText = 'Please select an image and ask a question.';
    }
    
});

questionInput.addEventListener('keydown', function(event) {
    /* Add an event listener to the question input field
        Concretely, it will execute the questions immediately and unfocus this 
        question box when the users press only 1 Enter key.
        Beside that, it will break the line if the users hold Shift and press Enter.
    */
   
    // Check if the "Enter" key was pressed
    if (event.key === 'Enter') {
      // Check if the "Shift" key was held down
      if (event.shiftKey) {
        // Insert a line break character into the question input field
        const cursorPosition = this.selectionStart;
        const oldValue = this.value;
        const newValue = oldValue.substring(0, cursorPosition) + '\n' + oldValue.substring(cursorPosition);
        this.value = newValue;
        this.selectionStart = this.selectionEnd = cursorPosition + 1;
        // Prevent the default action of the "Enter" key (submitting a form)
        event.preventDefault();
      } else {
        // Prevent focusing on the question input and submitting the form
        this.blur();
        submitButton.click();
      }
    }
  });



  function showTextInput(event) {
      textInput.style.display = "block";
      imageInput.style.display = "none";
      is_text = true;
      event.preventDefault();
  }

  function showImageInput(event) {
      fileInput.type = "file";
      fileInput.accept = "image/*";
      fileInput.addEventListener("change", handleImageUpload);
      fileInput.click();
      is_text = false;
      event.preventDefault();

      
  }

  function handleImageUpload(event) {
      const file = event.target.files[0];
      if (!file.type.startsWith("image/")) {
          alert("Please select an image file.");
          return;
      }
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onloadend = function () {
          imageInput.src = reader.result;
          imageInput.style.display = "block";
          textInput.style.display = "none";
      };
  }

const instructions = "1. Select type of context you want to provide (text/image) \n 2. If text, type or copy to context field. \n If image, select image from you device to upload to system \n 3. Type or copy to question field (the content should be related to provided context)\n You can input multiple question (as long as they are separated by '?') 4. Wait for the answer \n 5. Give feedback about question" 

const helpButton = document.getElementById('help-button');
helpButton.addEventListener('click', function() {
  
        var maxHeight = $(window).height() - 200;
        var maxWidth = $(window).width() - 200;
        const popupCard = $('<div>').addClass('popup-card');
        const closeButton = $('<button>').text('X');
        const answerTitle = $('<h2>').text('Here is the instruction');
        const answerText = $('<p>').text(instructions);

        closeButton.click(() => {
            popupCard.remove();
        });

        popupCard.append(closeButton);
        popupCard.append(answerTitle);
        popupCard.append(answerText);
        $('body').append(popupCard);

        // Adjust the size of the popup card if necessary
        const popupCardHeight = popupCard.height();
        const popupCardWidth = popupCard.width();

        if (popupCardHeight > maxHeight) {
            popupCard.height(maxHeight);
            popupCard.width(maxHeight * popupCardWidth / popupCardHeight);
        }

        if (popupCardWidth > maxWidth) {
            popupCard.width(maxWidth);
            popupCard.height(maxWidth * popupCardHeight / popupCardWidth);
        }
});



