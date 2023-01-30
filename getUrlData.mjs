import axios, { Axios } from 'axios';

export function getWeather(city, uk = 'ru') {
   return axios.get(`https://api.openweathermap.org/data/2.5/weather?q=${city},${uk}&APPID=${process.env.WEATHERTOKEN}&units=metric`)
      .then(res => res.data)
      .catch(error => console.error(error))
};
