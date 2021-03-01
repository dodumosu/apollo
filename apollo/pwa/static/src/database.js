import Dexie from 'dexie';

class LocalDatabase extends Dexie {
    constructor() {
        super('apollo');

        this.version(1).stores({
            forms: 'id, participant_id',
            participants: 'participant_id, lastLogin',
            submissions: '++id, participant_id, [id+participant_id], form, posted, updated'
        });

        this.forms = this.table('forms');
        this.participants = this.table('participants');
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

    getSubmissions(participant_id) {
        return this.submissions.where({participant_id: participant_id}).toArray();
    }

    saveForms(forms) {
        return this.transaction('rw', this.forms, () => {
            this.forms.bulkPut(forms);
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
};

export default LocalDatabase;
