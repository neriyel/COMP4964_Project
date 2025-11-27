#!groovy
import jenkins.model.Jenkins
import hudson.security.HudsonPrivateSecurityRealm
import hudson.security.FullControlOnceLoggedInAuthorizationStrategy

def instance = Jenkins.getInstance()

try {
    println("Setting up Jenkins security...")
    
    def realm = new HudsonPrivateSecurityRealm(false)
    realm.createAccount("admin", "admin123")
    instance.setSecurityRealm(realm)
    
    def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
    instance.setAuthorizationStrategy(strategy)
    
    instance.save()
    println("✓ Jenkins initialized with admin user: admin / admin123")
} catch (Exception e) {
    println("✓ Jenkins security already configured or error: ${e.message}")
}
