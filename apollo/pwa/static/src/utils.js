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

export { formSorter };
