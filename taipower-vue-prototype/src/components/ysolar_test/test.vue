<template>

</template>

<script>
export default {
    name: "test1",
	components: {
	},
	data() {
		return {
			test_data:'',
		};
	},
	method:{
		button1_clicked(){
			function inner_function(){
				var a = '123'
				this.test_data = a
			}
			inner_function()
		},
		button2_clicked(){
			console.log(this.test_data)
		}
	},
	watch: {
		test_data:{
			handler:function(){
				console.log('change detected')
			},
			deep: true
		}
	},
};
</script>


<!-- 設定css的部分(樣式) -->
<style scoped>
</style>