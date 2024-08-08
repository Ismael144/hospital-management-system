
// $(function () {
// 	'use strict';

// 	$('#data-table').DataTable({
// 		'paging': true,
// 		'lengthChange': false,
// 		'searching': true,
// 		'ordering': true,
// 		'info': true,
// 		'autoWidth': false,
// 		buttons: [
// 			'copy', 'csv', 'excel', 'pdf', 'print'
// 		]
// 	});
// }); 

$('#data-table').DataTable( {
	dom: 'Bfrtip',
    paging: true,
    lengthChange: false,
    searching: true,
    ordering: true,
    info: true,
    autoWidth: false,
	buttons: [
		'copy', 'csv', 'excel', 'pdf', 'print'
	]
} );

// End of use strict
    // // Setup - add a text input to each footer cell
    // $('#data-table tfoot th').each( function () {
    //     var title = $(this).text();
    //     $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
    // } );
 
    // // DataTable
    // var table = $('#data-table').DataTable();
 
    // // Apply the search
    // table.columns().every( function () {
    //     var that = this;
 
    //     $( 'input', this.footer() ).on( 'keyup change', function () {
    //         if ( that.search() !== this.value ) {
    //             that
    //                 .search( this.value )
    //                 .draw();
    //         }
    //     } );
    // } );

$(function () {
	'use strict';

	$('#data-table-1').DataTable({
		'paging': true,
		'lengthChange': false,
		'searching': true,
		'ordering': true,
		'info': true,
		'autoWidth': false
	});
}); // End of use strict
