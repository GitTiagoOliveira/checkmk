CHECK_CERT := check-cert
CHECK_CERT_PACKAGE := $(REPO_PATH)/packages/$(CHECK_CERT)
CHECK_CERT_RELEASE := $(CHECK_CERT_PACKAGE)/target/release/check_cert

CHECK_CERT_BUILD := $(BUILD_HELPER_DIR)/$(CHECK_CERT)-build
CHECK_CERT_INSTALL := $(BUILD_HELPER_DIR)/$(CHECK_CERT)-install

.PHONY: $(CHECK_CERT_BUILD)
$(CHECK_CERT_BUILD): $(OPENSSL_INTERMEDIATE_INSTALL)
	RUST_BACKTRACE=full \
	OPENSSL_DIR="$(OPENSSL_INSTALL_DIR)" \
	OPENSSL_LIB_DIR="$(OPENSSL_INSTALL_DIR)/lib" \
	OPENSSL_INCLUDE_DIR="$(OPENSSL_INSTALL_DIR)/include" \
	$(CHECK_CERT_PACKAGE)/run --build
	# set RPATH
	patchelf --set-rpath "\$$ORIGIN/../../../lib" $(CHECK_CERT_RELEASE)
	$(TOUCH) $@

.PHONY: $(CHECK_CERT_INSTALL)
$(CHECK_CERT_INSTALL): $(CHECK_CERT_BUILD)
	install -m 755 $(CHECK_CERT_RELEASE) $(DESTDIR)$(OMD_ROOT)/lib/nagios/plugins/
	$(TOUCH) $@
