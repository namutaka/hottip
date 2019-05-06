export const SCHEDULE_TEXT = [
  ['month', '月'],
  ['day', '日'],
  ['hour', '時'],
  ['minute', '分'],
  ['day_of_week', '曜日'],
];

export const DAY_OF_WEEK_TEXT = ['月', '火', '水', '木', '金', '土', '日'];

export function scheduleText(schedule_str: string): string {
  const schedule = JSON.parse(schedule_str);

  let caption = [];
  for (let [field, label] of SCHEDULE_TEXT) {
    let text = '';

    if (field != 'day_of_week') {
      const [val, step] = schedule[field].toString().split('/', 2);
      if (val == '*') {
        text += '毎' + label;
      } else {
        if (field == 'day') {
          let match = val.match('(last|[0-9]th) ([0-6])');
          if (match) {
            let weekday = DAY_OF_WEEK_TEXT[parseInt(match[2], 10)] + '曜日';
            if (match[1] == 'last') {
              text += '最終週' + weekday;
            } else {
              text += '第' + match[1].replace('th', '') + weekday;
            }
          } else if (val == 'last') {
            text += '最終日';
          } else {
            text += val + label;
          }
        } else {
          text += val + label;
        }
      }

      if (step) {
        text += step + label + '間隔';
      }
    } else {
      let dow = schedule['day_of_week'];
      if (dow != '*') {
        dow = dow.replace(/[0-6]/g, function(match: string) {
          return DAY_OF_WEEK_TEXT[parseInt(match, 10)];
        });
        text = dow + '曜日';
      }
    }

    caption.push(text);
  }

  return caption.join(' ');
}
