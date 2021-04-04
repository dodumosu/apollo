<script>
  export let forms, i18n, submissionCounts;
</script>

<div class="row">
  <div class="col">
    <div class="card shadow-sm mt-3">
      <h5 class="card-header">{ i18n.gettext('Forms') }</h5>
        <div class="list-group list-group-flush">
          {#each forms as form}
            <div class="row">
              <div class="col mb-2">{ form.name } <span class="badge bg-secondary">{ forms.form_type }</span> {#if form.form_type !== 'CHECKLIST'} <span class="badge bg-dark">{ submissionCounts[form.id] || 0 }</span> {/if}</div>
            </div>
            <div class="row">
              <div class="col mb-2"></div>
            </div>
          {/each}
        </div>
    </div>
  </div>
</div>