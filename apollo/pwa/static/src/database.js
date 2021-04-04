import Dexie from 'dexie';

class ApolloDatabase extends Dexie {
  constructor() {
    super('apollo');

    this.version(1).stores({
      forms: 'id, participant_id',
      participants: 'participant_id, lastLogin',
      submissions: '++id, participant_id, [id+participant_id], form, posted, updated'
    });

    this.version(2).stores({
      serials: 'form, participant_id, [form+participant_id]'
    });

    this.forms = this.table('forms');
    this.participants = this.table('participants');
    this.serials = this.table('serials');
    this.submissions = this.table('submissions');
  }

  getForms(participant_id) {
    return this.forms.where({participant_id: participant_id}).toArray();
  }

  async getParticipant() {
    let participants = await this.participants.toCollection().reverse().sortBy('lastLogin');

    if (participants.length !== 0)
      return participants[0];
    
    return null;
  }

  getSubmissions(participant_id, form_id = null) {
    let queryTerm = form_id === null ? {participant_id: participant_id} : {participant_id: participant_id, form: form_id};
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

export default ApolloDatabase;
