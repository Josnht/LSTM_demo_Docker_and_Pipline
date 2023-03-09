pipeline{
    agent{
        label "node"
    }
    stages{
        stage("clone"){
            steps{
                checkout scm
            }
        }
    }
    stage('Build Image') {
	        steps {
	        sh 'docker build -t lstm .'
	        }
	   }
    stage('Testing'){
	        steps {
	            echo 'Testing..'
	            }
	   }
}
