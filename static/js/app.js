const form1 = document.querySelector('#form-1');
const form2 = document.querySelector('#form-2');

$(document).ready(function () {
	fetch('http://127.0.0.1:5000/api/resrecommender/restaurants')
		.then(response => response.json())
		.then(data => {
			var content = data;
			$('.ui.search')
				.search({
					source: content,
					searchFields: [
						'name', 'location'
					],
					fullTextSearch: false,
					fields: {
						title: 'name',
						description: 'location'
					},
					// onSelect: function (result, response) {
					// 	console.log(result)
					// 	var restaurant_name = result.name;
					// 	searchbox = document.querySelector("#searchbox");
					// 	searchbox.removeAttribute("value");
					// 	searchbox.setAttribute("value", restaurant_name);
					// 	console.log(searchbox);
					// 	console.log(searchbox.value);
					// 	// form1.submit();
					// 	return true;
					// }
				});
		});

	
	fetch('http://127.0.0.1:5000/api/resrecommender/cuisines')
		.then(response => response.json()
		.then(data => {
			$('.ui.dropdown')
			.dropdown({
				values: data,
				fields: {
					name: 'name',
					value: 'value'
				},
				placeholder: 'Select cuisines',
				// onChange: (a,b,c) => {
				// 	console.log($('.ui.dropdown').dropdown('get values'));
				// }
			});
		})
		);
});

form2.addEventListener("submit", e => {
	e.preventDefault();
	// console.log($('.ui.dropdown').dropdown('get values'));
	cuisines = $('.ui.dropdown').dropdown('get values');
	let options = {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(cuisines)
	}
	if (cuisines.length > 0) {
		form2.submit();
	}
	fetch('http://127.0.0.1:5000/api/resrecommender/2', options)
		.then(response => response.json()
		.then(data => {
			console.log(data)
		}
		))
});