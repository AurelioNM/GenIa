import http from 'k6/http';
import { check } from 'k6';
import * as util from '../util/util.js';

export const options = {
	vus: 5,
	duration: '20s',
};

export default function() {
	const url = `${util.weatherBaseUrl}/v1/weathers/cities/Rio%20de%20Janeiro`

	const res = http.get(url)
	check(res, {
		'status 200': (r) => r.status === 200
	})
}