class AppDatabase extends Dexie {
  constructor() {
    super('apollo');

    this.version(1).stores({
      forms: 'id, participant_id',
      participants: 'participant_id, lastLogin',
      submissions: '++id, participant_id, [id+participant_id], form, queuedAt, postedAt, [form+participant_id]',
      serials: '[form+participant_id+serial], [form+participant_id], form, participant_id, serial'
    });
  }

  getForms(participant_id) {
    return this.forms.where({ participant_id: participant_id }).toArray().then(forms => forms.sort(formSorter));
  }

  async getLastParticipant() {
    let participants = await this.participants.toCollection().reverse().sortBy('lastLogin');

    if (participants.length !== 0)
      return participants[0];

    return null;
  }

  getSubmissions(participant_id, formId = null) {
    let queryTerm = {participant_id: participant_id};
    if (formId !== null)
      queryTerm.form = formId;
    
    return this.submissions.where(queryTerm).toArray();
  }

  saveForms(forms) {
    return this.transaction('rw', this.forms, () => {
      this.forms.bulkPut(forms);
    });
  }

  saveSerials(serials) {
    return this.transaction('rw', this.serials, () => {
      this.serials.bulkPut(serials);
    });
  }

  saveParticipant(participant) {
    return this.transaction('rw', this.participants, () => {
      this.participants.put(participant);
    });
  }

  saveSubmission(submission) {
    return this.transaction('rw', this.submissions, () => {
      this.submissions.put(submission);
    });
  }
}