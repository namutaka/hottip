import { KeyValue } from '@/types/models';
import { DistributorType } from '../../types/globalTypes';

export class Attribute {
  constructor(private attribute: KeyValue[]) {}

  get(key: string) {
    let kv = this.attribute.find(kv => kv.key == key);
    return kv ? kv.value : '';
  }

  set(key: string, value: string) {
    let kv = this.attribute.find(kv => kv.key == key);
    if (kv) {
      kv.value = value;
    } else {
      this.attribute.push({ key, value });
    }
  }
}

export const ATTRIBUTE_FIELDS = {
  [DistributorType.SLACK] : [
    {
      key: 'channel',
      label: '送信先チャンネル名',
      placeholder: '例) @username #general',
    },
    {
      key: 'username',
      label: '送信Botのユーザ名',
      placeholder: ' ',
    },
    {
      key: 'icon',
      label: '送信Botのアイコン',
      placeholder: '例) :ghost:',
    }
  ]
};
