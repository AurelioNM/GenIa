import http from 'k6/http';
import { check } from 'k6';
import * as util from '../util/util.js';

export const options = {
	vus: 5,
	duration: '20s',
};

export default function() {
	const url = `${util.weatherBaseUrl}/v2/weathers/cities?page=1&size=10`

	const res = http.get(url)
	check(res, {
		'status 200': (r) => r.status === 200
	})
}