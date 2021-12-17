const AWS = require('aws-sdk');
const SES = new AWS.SES();

const FROM_EMAIL_ADDRESS = process.env.FROM_EMAIL_ADDRESS;
const TO_EMAIL_ADDRESS = process.env.TO_EMAIL_ADDRESS;

function sendEmailToMe(formData) {

    const emailParams = {
        Source: FROM_EMAIL_ADDRESS,
        ReplyToAddresses: ['testReply@email.com'],
        Destination: {
          ToAddresses: [TO_EMAIL_ADDRESS],
        },
        Message: {
          Body: {
            Text: {
              Charset: 'UTF-8',
              Data: `Dear user,\n${formData.message}\n\n Regards,\n Aquarium Paradise`,
            },
          },
          Subject: {
            Charset: 'UTF-8',
            Data: `${formData.subject}`,
          },
        },
    };

    console.log(emailParams)

    const promise =  SES.sendEmail(emailParams).promise();
    console.log(promise);
    return promise
}


exports.sendEmail = async(event) => {
    console.log('Send email called');

    const dynamodb = event.Records[0].dynamodb;
    console.log(dynamodb);

    const formData = {
        message : dynamodb.NewImage.message.S,
        subject : dynamodb.NewImage.subject.S
    }
    console.log(formData);

    return sendEmailToMe(formData).then(data => {
        console.log(data);
    }).catch(error => {
        console.log(error);
    });
}