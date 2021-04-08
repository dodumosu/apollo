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

const computeGroupCompletion = (form, submission, groupIndex) => {
  let group = form.data.groups[groupIndex];

  let completion = {total: group.fields.length};
  completion.filled = group.fields.reduce((acc, field) => {
    if (field.type === 'image')
      acc += (submission.images[field.tag] !== undefined ? 1 : 0);
    else if (field.type === 'multiselect')
      acc += (submission.data[field.tag].length > 0 ? 1: 0);
    else
      acc += (submission.data[field.tag] !== undefined ? 1 : 0);

    return acc;
  }, 0);

  return completion;
};

const formCompletion = (form, submission) => form.data.groups.map((_, index) => computeGroupCompletion(form, submission, index));

const formCompletionAsObject = (form, submission) => formCompletion(form, submission).reduce((acc, completion) => {
  acc[filled] += completion.filled;
  acc[total] += completion.total;

  return acc;
}, {total: 0, filled: 0});

export { computeGroupCompletion, formSorter, formCompletion, formCompletionAsObject };
