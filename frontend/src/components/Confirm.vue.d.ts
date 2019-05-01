
export = Confirm;

declare class Confirm {
  static open(title: string, message: string, options?: any): Promise<boolean>
}
