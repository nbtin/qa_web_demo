const fileInput = document.getElementById('file-input');
const questionInput = document.getElementById('question-input');
const submitButton = document.getElementById('submit-button');
const answerElement = document.getElementById('answer');
const imageElement = document.getElementById('image');

fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.addEventListener('load', () => {
            imageElement.src = reader.result;
        });
        reader.readAsDataURL(file);
    }
});

submitButton.addEventListener('click', (event) => {
    event.preventDefault();
    const file = fileInput.files[0];
    const question = questionInput.value;
    answerElement.innerText = "Wait a second...";

    if (file && question) {
        const formData = new FormData();
        formData.append('image', file);
        formData.append('questions', question);

        fetch('/answer', {
        method: 'POST',
        body: JSON.stringify({
            image: imageElement.src,
            questions: questionInput.value
        }),
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
                if (lines.length > 1){
                    for (let i = 0; i < lines.length; i+=3){
                        let line_changed = '<b>' + lines[i] + '</b>';
                        if (i != 0) lines[i] = '<br>' + line_changed;
                        lines[i] = line_changed;
                    }
                    result = lines.join("<br>");
                    console.log(result);
                }
                answerElement.innerHTML = result;
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
        answerElement.innerText = 'Please select an image and ask a question.';
    }
});

// Add an event listener to the question input field
questionInput.addEventListener('keydown', function(event) {
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
        // Click the submit button to submit the form
        submitButton.click();
    }
}
});