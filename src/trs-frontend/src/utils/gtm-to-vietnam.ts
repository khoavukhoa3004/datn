
export function convertToVietnamTime(gmtDateTime: string): string {
    const gmtDate = new Date(gmtDateTime);
    const vietnamOffset = 7; // Vietnam is UTC+7
  
    // Add the offset to the GMT date
    const vietnamDate = new Date(gmtDate.getTime() + vietnamOffset * 60 * 60 * 1000);
  
    // Format the date and time as a string
    const options: Intl.DateTimeFormatOptions = {
      weekday: 'short',
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: 'numeric',
      second: 'numeric',
      timeZone: 'Asia/Ho_Chi_Minh', // Set the time zone to Vietnam
    };
    const vietnamDateTime = vietnamDate.toLocaleString('en-US', options);
  
    return vietnamDateTime;
  }