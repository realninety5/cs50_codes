let emails_view = document.querySelector('#emails-view')
let mail_template = document.getElementById('mail-template')


function check_parent(e){
	return e.id || e.parentNode.id || e.parentNode.parentNode.id;
}

// Read or unread an email
function read_unread(mail_id, action){
    let todo = (action == 'read') ? true : false;
    fetch(`emails/${mail_id}`,{
        method: 'PUT',
        body: JSON.stringify({
            read: todo
        })
    })
}

// Archive or unarchive an email
function archive(mail_id, action){
    let todo = (action == 'archive') ? true : false;
    fetch(`emails/${mail_id}`,{
        method: 'PUT',
        body: JSON.stringify({
            archived: todo
        })
    })
}


function open_email(mail_id) {
    document.querySelector('#emails-view').style.display = 'none';
    document.getElementById('mail-template').style.display = 'none';
    setTimeout(() =>
        {
            document.getElementById('mail-template').style.display = 'block';
        },
        300
    );
    document.querySelector('#compose-view').style.display = 'none';
    fetch(`emails/${mail_id}`).then(
	response => response.json())
    .then(result =>
	{        
		let mail = `<div><strong>From</strong>: ${result['sender']}</div>`;
        mail += `<div><strong>To</strong>: ${result['recipients']}</div>`;
        mail += `<div><strong>Subject</strong>: ${result['subject']}</div>`;
        mail += `<div><strong>Timestamp</strong>: ${result['timestamp']}</div>`;
        if (window.mail_title != 'Sent'){
            mail += '<p><input value="Reply" type="submit" class="btn btn-sm btn-outline-primary" id="reply"/>'
        mail += `<input id="${mail_id}" value="Unread" type="submit" class="btn btn-sm btn-outline-primary read" style="float: right;"/>`
            mail += `<input value="" id="${mail_id}" type="submit" class="btn btn-sm btn-outline-primary archive" style="float: right; margin-right: 5px;"/></p>`
        }
        mail += '<hr>'
        mail += `${result['body']}`
        mail_template.innerHTML = mail;
        declare_results(result);
        let arch = document.querySelector('.archive');
        if (window.mail_title != 'Sent'){
            if (result['archived'] == true) {
                arch.value = 'Unarchive';
            }else if (arch.value == ""){
                arch.value = "Archive";
            }
        }
	})
    read_unread(mail_id, 'read');

}

// Declare the returned value from fetch email above
function declare_results(value){
    window.results = value;
}

// Event to track if the 'reply' button was clicked
mail_template.addEventListener('click', e => {
    if (e.target.id === 'reply'){
        window.tops = `${window.results['sender']}`;
        window.subject = `${window.results['subject']}`;
        window.body = `${window.results['body']}`;
        window.date = `${window.results['timestamp']}`;
        compose_email(window.tops, window.subject, window.body, window.date);
    }
    else if (e.target.value == 'Unread') {
        read_unread(parseInt(e.target.id), 'unread')
        e.target.value = 'Read';
    }
    else if (e.target.value == 'Read') {
        read_unread(parseInt(e.target.id), 'read')
        e.target.value = 'Unread';
    }
    else if (e.target.value == 'Unarchive') {
        archive(parseInt(e.target.id), 'unarchive')
        e.target.value = 'Archive';
    }
    else if (e.target.value == 'Archive') {
        archive(parseInt(e.target.id), 'archive')
        e.target.value = 'Unarchive';
    }
});

document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);

    // By default, load the inbox
    load_mailbox('inbox');
});

function compose_email(receiver, subject, body, date) {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.getElementById('mail-template').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Clear out composition fields
    if (typeof receiver != 'string') {

        document.querySelector('#compose-recipients').value = '';
        document.querySelector('#compose-subject').value = '';
        document.querySelector('#compose-body').value = '';
    } else {
        document.querySelector('#compose-recipients').value = receiver;
        document.querySelector('#compose-subject').value = 'Re: ' + subject;
        document.querySelector('#compose-body').value = `On ${date} ${receiver} wrote: ` + body;
    }
}

document.querySelector('#compose-form').addEventListener('submit', (e) => {
    document.querySelector('#compose-recipients').value;
    let recipients = document.querySelector('#compose-recipients').value;
    let subject = document.querySelector('#compose-subject').value;
    let body = document.querySelector('#compose-body').value;


    e.preventDefault();
    // Send mail to the backend
    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: recipients,
            subject: subject,
            body: body
        })
    }).then(response => response.json())
    .then(result => {console.log(result)})
    
    setTimeout(() =>
        {
            load_mailbox('sent')
        },
        300
    );
});

function load_mailbox(mailbox) {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.getElementById('mail-template').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';

    // Show the mailbox name and get its textContent
    document.querySelector('#emails-view').innerHTML = `<h3 class="mail-title">${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
    window.mail_title = document.querySelector('.mail-title').textContent
    // Retrieve user's sent emails
    fetch(`/emails/${mailbox}`).then(response => response.json())
    .then(emails => {
        emails.forEach( email => {
            let div_top = document.createElement('div')
            let div = document.createElement('div')
            div.className = 'mail-boxs';
            if (window.mail_title != 'Sent'){
                if (email['read'] === true){
                div.style.backgroundColor = '#DCDCDC';
                }else {
                div.style.backgroundColor = 'white';
                }
            }
            div.id = `${email['id']}`;
            div.style.border = 'solid 1px gray';
            div.style.padding = '8px';
            let email_sub = document.createElement('span')
            email_sub.className = 'mail-boxs';
            email_sub.innerHTML = `<strong class="mail-boxs">${email['sender']}</strong>  ${email['subject']}`
            let time_stamp = document.createElement('span')
            time_stamp.innerHTML = `${email['timestamp']}`
            time_stamp.className = 'mail-boxs';
            time_stamp.style.float = 'right';
            div_top.className = 'move';
            div.appendChild(email_sub);
            div.appendChild(time_stamp);
            div_top.append(div);
            emails_view.appendChild(div_top);
        });
    });
}


// Event to get the div element (message) that
// was clicked
emails_view.addEventListener('click', e => {
    if (e.target.className == 'mail-boxs'){
        let mail_id = check_parent(e.target);
    open_email(parseInt(mail_id))
    }
})

