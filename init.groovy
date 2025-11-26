#!groovy
import jenkins.model.Jenkins
import hudson.security.HudsonPrivateSecurityRealm
import hudson.security.FullControlOnceLoggedInAuthorizationStrategy

def jenkins = Jenkins.getInstance()

// Create admin user if it doesn't exist
def realm = new HudsonPrivateSecurityRealm(false)
def adminUser = realm.createAccount('admin', 'admin123')
jenkins.setSecurityRealm(realm)

// Set authorization strategy
def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
jenkins.setAuthorizationStrategy(strategy)

jenkins.save()
println("Jenkins initialized with admin user: admin / admin123")
