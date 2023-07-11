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
        fetch('/answer', {
        method: 'POST',
        body: JSON.stringify(input),
        headers: {
            'Content-Type': 'application/json'
        }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                let result = data.data;
                console.log(result);
                const lines = result.split("\n");
                console.log(lines);
                
                if (lines.length > 1){ // change the format of result for multi-answer cases.
                    for (let i = 0; i < lines.length; i+=3){    
                        let line_changed = '<b>' + lines[i] + '</b>';
                        if (i != 0) lines[i] = '<br>' + line_changed;
                        lines[i] = line_changed;
                    }
                    result = lines.join("<br>");
                    console.log(result);
                }
                answerBox.innerHTML = result;
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