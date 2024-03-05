import dfd from 'danfojs-node';
import Chart from 'chart.js/auto';
import { createCanvas, loadImage } from 'canvas';
import fs from 'fs/promises';
import { join } from 'path';

// https://beta.data.gov.sg/datasets/d_3c55210de27fcccda2ed0c63fdd2b352/view
const raw_data = await dfd.readCSV(join(process.cwd(), 'datasets', 'grad_pay.csv'));

const data2013 = raw_data.loc({
	rows: raw_data['year'].values.map((year) => year === 2013),
});
const data2021 = raw_data.loc({
	rows: raw_data['year'].values.map((year) => year === 2021),
});

console.log('2013 data');
data2013.head().print();
console.log('2021 data');
data2021.head().print();

// they're apparently all unique but anyways
const degrees = [...new Set(raw_data['degree'].values)];
let degreeChanges = new dfd.DataFrame([['', 0, 0, 0]], { columns: ['degree', '2013', '2021', 'change/%'] });


// get % change in pay for each degree
let index = 0;
for (const degree of degrees) {
	index++;
	const pay_2013_data = data2013.loc({
		rows: data2013['degree'].values.map((d) => d === degree),
	})['basic_monthly_mean'];
	const pay_2013 = pay_2013_data.values.length > 0 ? pay_2013_data.mean() : undefined;

	const pay_2021_data = data2021.loc({
		rows: data2021['degree'].values.map((d) => d === degree),
	})['basic_monthly_mean'];
	const pay_2021 = pay_2021_data.values.length > 0 ? pay_2021_data.mean() : undefined;

	const percent_change = ((pay_2021 - pay_2013) / pay_2013) * 100 ?? undefined;

	degreeChanges = degreeChanges.append([[degree, pay_2013, pay_2021, percent_change]], [index]);

	// if (pay_2013 && pay_2021) {
	// 	// console.log(pay_2013, pay_2021, percent_change.toFixed(2));
	// 	// console.log(`% change in pay for ${degree} from 2013 to 2021: ${percent_change.toFixed(2)}%`);
	// 	// console.log(`2013 mean pay for ${degree}: ${pay_2013.toFixed(2)}`);
	// 	// console.log(`2021 mean pay for ${degree}: ${pay_2021.toFixed(2)}`);
	// 	// inplace is apparently broken
	// 	degreeChanges = degreeChanges.append([[degree, pay_2013, pay_2021, percent_change]], [index]);
	// }
	// else {
	// 	degreeChanges = degreeChanges.append([[degree, pay_2013 ? pay_2013.toFixed(2) : undefined, pay_2021 ? pay_2021.toFixed(2) : undefined, undefined]], [index]);
	// }
}

// remove the first row
degreeChanges = degreeChanges.loc({ rows: degreeChanges['$index'].map((i) => i !== 0) });

// degreeChanges.print();

// drop undefined values
degreeChanges = degreeChanges.dropNa();

// sort by % change
degreeChanges = degreeChanges.sortValues('change/%', { ascending: false });

console.log('Degree changes');
degreeChanges.print();

// get top 5 and bottom 5

const top3 = degreeChanges.head(3);
const bottom3 = degreeChanges.tail(3);

console.log('Top 3');
top3.print();
console.log('Bottom 3');
bottom3.print();

// plot the data
// const canvas = createCanvas(800, 800);
// const ctx = canvas.getContext('2d');

// const chart = new Chart(ctx, {
// 	type: 'bar',
// 	data: {
// 		labels: top3['degree'].values,
// 		datasets: [
// 			{
// 				label: '% change in pay',
// 				data: top3['change/%'].values,
// 				backgroundColor: 'rgba(75, 192, 192, 0.5)',
// 				borderColor: 'rgba(75, 192, 192, 1)',
// 				borderWidth: 1,
// 			},
// 		],
// 	},
// 	options: {
// 		scales: {
// 			y: {
// 				beginAtZero: true,
// 			},
// 		},
// 	},
// });

// create /output directory if it doesn't exist
try {
	await fs.access(join(process.cwd(), 'output'));
}
catch (err) {
	if (err.code === 'ENOENT') {
		await fs.mkdir(join(process.cwd(), 'output'));
	}
}

// save the chart
// const chartPath = join(process.cwd(), 'output', 'd2_a1_q1_chart.png');
// const out = canvas.createPNGStream();
// const file = await fs.open(chartPath, 'w+');
// const writeStream = file.createWriteStream();
// out.pipe(writeStream);
// writeStream.on('finish', () => {
// 	console.log(`Chart saved to ${chartPath}`);
// 	file.close();
// });
// writeStream.on('error', (err) => {
// 	console.error(err);
// });

// plot the highest and lowest changes (top 1)
const top1 = degreeChanges.head(1);
const bottom1 = degreeChanges.tail(1);


// plot the data using a line chart
const canvas2 = createCanvas(800, 800);
const ctx2 = canvas2.getContext('2d');

const chart2 = new Chart(ctx2, {
	type: 'line',
	data: {
		labels: ['2013', '2021'],
		datasets: [
			{
				label: top1['degree'].values[0],
				data: [top1['2013'].values[0], top1['2021'].values[0]],
				fill: false,
				borderColor: 'rgba(75, 192, 192, 1)',
				tension: 0.1,
			},
			{
				label: bottom1['degree'].values[0],
				data: [bottom1['2013'].values[0], bottom1['2021'].values[0]],
				fill: false,
				borderColor: 'rgba(192, 75, 75, 1)',
				tension: 0.1,
			},
		],
	},
	options: {
		scales: {
			y: {
				beginAtZero: true,
			},
		},
	},
});

// save the chart
const chartPath2 = join(process.cwd(), 'output', 'd2_a1_q2_chart.png');
const out2 = canvas2.createPNGStream();
const file2 = await fs.open(chartPath2, 'w+');
const writeStream2 = file2.createWriteStream();
out2.pipe(writeStream2);
writeStream2.on('finish', () => {
	console.log(`Chart saved to ${chartPath2}`);
	file2.close();
});
writeStream2.on('error', (err) => {
	console.error(err);
});

// https://tablebuilder.singstat.gov.sg/table/TS/M212911
const cpi_pct_increase = await dfd.readCSV(join(process.cwd(), 'datasets', 'cpi_pct_increase.csv'));
// https://tablebuilder.singstat.gov.sg/table/TS/M212882
const cpi = await dfd.readCSV(join(process.cwd(), 'datasets', 'cpi.csv'));


const cpiData = cpi.drop({ columns: ['Data Series'] });
const cpiYears = cpiData.columns;
const cpiValues = cpiData.values[0];

const canvas3 = createCanvas(800, 800);
const ctx3 = canvas3.getContext('2d');

const chart3 = new Chart(ctx3, {
	type: 'line',
	data: {
		labels: cpiYears,
		datasets: [
			{
				label: 'CPI',
				data: cpiValues,
				fill: false,
				borderColor: 'rgba(75, 192, 192, 1)',
				tension: 0.1,
			},
		],
	},
	options: {
		scales: {
			y: {
				beginAtZero: false,
			},
		},
	},
});

// save the chart
const chartPath3 = join(process.cwd(), 'output', 'd2_a1_q3_chart.png');
const out3 = canvas3.createPNGStream();
const file3 = await fs.open(chartPath3, 'w+');
const writeStream3 = file3.createWriteStream();
out3.pipe(writeStream3);
writeStream3.on('finish', () => {
	console.log(`Chart saved to ${chartPath3}`);
	file3.close();
});

// plot cpi % increase

const cpiPctIncreaseData = cpi_pct_increase.drop({ columns: ['Data Series'] });
const cpiPctIncreaseYears = cpiPctIncreaseData.columns;
const cpiPctIncreaseValues = cpiPctIncreaseData.values[0];

const canvas4 = createCanvas(800, 800);
const ctx4 = canvas4.getContext('2d');

const chart4 = new Chart(ctx4, {
	type: 'line',
	data: {
		labels: cpiPctIncreaseYears,
		datasets: [
			{
				label: 'CPI % increase',
				data: cpiPctIncreaseValues,
				fill: false,
				borderColor: 'rgba(75, 192, 192, 1)',
				tension: 0.1,
			},
		],
	},
	options: {
		scales: {
			y: {
				beginAtZero: false,
			},
		},
	},
});

// save the chart
const chartPath4 = join(process.cwd(), 'output', 'd2_a1_q4_chart.png');
const out4 = canvas4.createPNGStream();
const file4 = await fs.open(chartPath4, 'w+');

const writeStream4 = file4.createWriteStream();
out4.pipe(writeStream4);
writeStream4.on('finish', () => {
	console.log(`Chart saved to ${chartPath4}`);
	file4.close();
});
writeStream4.on('error', (err) => {
	console.error(err);
});
