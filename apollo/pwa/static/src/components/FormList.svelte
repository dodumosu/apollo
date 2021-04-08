<script>
  import { onMount } from 'svelte/internal';

  export let db, i18n, participant;
  let forms = [];
  let submissions = [];
  let submissionCounts = {};
  let submissionGroups = {};

  onMount(async () => {
    db.getForms(participant.participant_id).then(dbForms => {
      forms = dbForms;
    });

    db.getSubmissions(participant.participant_id).then(subs => {
      submissions = subs;

      submissionGroups = submissions.reduce((acc, sub) => {
        acc[sub.form] = acc[sub.form] || [];
        acc[sub.form].push(sub);

        return acc;
      }, {});
      submissionCounts = Object.keys(submissionGroups).reduce((acc, formId) => {
        acc[formId] = submissionGroups[formId].length;

        return acc;
      }, {});
    });
  });
</script>

<div class="row">
  <div class="col">
    <div class="card shadow-sm mt-3">
      <h5 class="card-header">{ i18n.gettext('Forms') }</h5>
        <div class="list-group list-group-flush">
          {#each forms as form, index}
            <div class="list-group-item">
              <div class="row">
                <div class="col mb-2">{ form.name } <span class="badge bg-secondary">{ form.form_type }</span> {#if form.form_type !== 'CHECKLIST'} <span class="badge bg-dark">{ submissionCounts[form.id] || 0 }</span> {/if}</div>
              </div>
              {#if form.form_type !== 'CHECKLIST'}
              <div class="row">
                <div class="col mb-2">
                  <div class="card mt-2">
                    <h5 class="card-header"><a href="{`#sub-list-${index}`}" data-bs-toggle="collapse" role="button">{#if form.form_type === 'INCIDENT' }{ i18n.gettext('Incidents') }{:else}{ i18n.gettext('Surveys') }{/if}</a></h5>
                    <div class="list-group list-group-flush collapse" id="{`#sub-list-${index}`}">
                      {#if submissionGroups[form.id]}
                      {#each submissionGroups[form.id] as submission, subIndex}
                        <div class="list-group-item">
                          <strong>{#if form.form_type === 'INCIDENT'}{ subIndex + 1 }{:else}{ submission.serial }{/if}</strong>
                        </div>
                      {/each}
                      {/if}
                    </div>
                  </div>
                </div>
              </div>
              {/if}
            </div>
          {/each}
        </div>
    </div>
  </div>
</div>