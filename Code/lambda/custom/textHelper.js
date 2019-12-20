'use strict';

var textHelper = (function () {

    return {
        myAPP_ID:                  'amzn1.echo-sdk-ams.app.71a193da-99a6-4b60-9b0c-75b361471657',

        onLaunchSpeechOutput:      'To hear the first thousand digits of pi say, digits of pi. You can say stop at any time',

        onLaunchRepromptSpeech:    'To hear the first thousand digits of pi say, digits of pi. You can say stop at any time',

        helpIntentSpeechOutput:    'To hear the first thousand digits of pi say, read digits of pi, or read pi. You can say stop, or cancel at any time as it might get annoying after a while',

        helpIntentRepromptSpeech:  'To hear the first thousand digits of pi say, read digits of pi, or read pi. You can say stop, or cancel at any time as it might get annoying after a while',

        stopIntentSpeechOutput:    'Goodbye, see you soon.',

        cancelIntentSpeechOutput:  'Goodbye, see you soon.'
    };
})();
module.exports = textHelper;
