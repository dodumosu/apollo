window.isUpdateAvailable = new Promise((resolve, reject) => {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/pwa/serviceworker.js', {scope: '/pwa/'})
      .then(registration => {
        console.log('service worker registered successfully with scope:', registration.scope);

        registration.onupdatefound = () => {
          const installingWorker = registration.installing;
          installingWorker.onstatechange = () => {
            switch (installingWorker.state) {
              case 'installed':
                if (navigator.serviceWorker.controller) {
                  // update available
                  resolve(true);
                } else {
                  // no update available
                  resolve(false);
                }

                break;
            }
          };
        };
      })
      .catch(error => console.error('service worker registration failed:', error));
  } else {
    console.error('Cannot use service workers');
  }
});


const formSorter = (a, b) => {
  const FORM_TYPE_MAP = {
    CHECKLIST: 1,
    SURVEY: 2,
    INCIDENT: 3
  };
  if (a.form_type !== b.form_type)
    return FORM_TYPE_MAP[a.form_type] - FORM_TYPE_MAP[b.form_type];

  if (a.name > b.name)
    return 1;
  else if (a.name < b.name)
    return -1;
  else
    return a.id - b.id;
};

