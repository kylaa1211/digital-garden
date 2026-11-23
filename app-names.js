// Finder may paste bundle extensions, release years, and companion launchers.
function normalizeAppName(value){
  return String(value).trim()
    .replace(/\.(app|exe|dmg|apk)$/i, '')
    .replace(/\s*\(20\d{2}\)$|[\s_-]+20\d{2}$/i, '')
    .replace(/^zoom(?:[ -]*launcher|\.us)$/i, 'Zoom')
    .trim();
}

function appNameKey(value){
  return normalizeAppName(value).replace(/^Adobe\s+/i, '').toLowerCase().replace(/[^a-z0-9]/g, '');
}

const MIN_TREE_APPS = 3;
const RELATED_CATEGORIES = [
  ['Creating things', 'Editing media', 'Collecting inspiration'],
  ['Archiving life', 'Capturing thoughts', 'Building knowledge'],
  ['Managing your device', 'Everyday tools', 'Surfing the web'],
  ['Getting around', 'Exploring nature', 'Fueling your body'],
  ['Watching and playing', 'Experiencing audio'],
  ['Buying things', 'Managing finances']
];

function groupTreeCategories(categories){
  const groups = categories.filter(category => category.apps.length)
    .map(category => ({...category, apps:[...category.apps]}));
  while (groups.length > 1){
    const index = groups.findIndex(group => group.apps.length < MIN_TREE_APPS);
    if (index < 0) break;
    const [small] = groups.splice(index, 1);
    const related = RELATED_CATEGORIES.find(names => names.includes(small.name)) || [];
    const target = groups.find(group => related.includes(group.name) && group.apps.length >= MIN_TREE_APPS)
      || groups.find(group => related.includes(group.name))
      || groups.find(group => group.apps.length >= MIN_TREE_APPS)
      || groups[0];
    target.apps.push(...small.apps);
  }
  return groups;
}
