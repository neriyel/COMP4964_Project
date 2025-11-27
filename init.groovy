#!groovy
import jenkins.model.Jenkins
import hudson.security.HudsonPrivateSecurityRealm
import hudson.security.FullControlOnceLoggedInAuthorizationStrategy

def instance = Jenkins.getInstance()

// Set up security if not already configured
if (instance.getSecurityRealm() instanceof hudson.security.SecurityRealm.DEFAULT) {
    println("Setting up Jenkins security...")
    
    def realm = new HudsonPrivateSecurityRealm(false)
    realm.createAccount("admin", "admin123")
    instance.setSecurityRealm(realm)
    
    def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
    instance.setAuthorizationStrategy(strategy)
    
    instance.save()
    println("✓ Jenkins initialized with admin user")
} else {
    println("✓ Jenkins security already configured")
}
