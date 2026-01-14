#
# Copyright (C) 2024 Savoir-faire Linux, Inc.
# SPDX-License-Identifier: GPL-3.0-only

import subprocess
import os


def init_app(app):

    @app.route('/api/scan/trigger', methods=['POST'])
    def trigger_scan():
        """
        Trigger a new scan by executing the scan.sh script.
        This will reset the scan and start a new one.
        """
        try:
            # The scan.sh script is located at /scan/src/scan.sh in the container
            scan_script = "/scan/src/scan.sh"
            if not os.path.exists(scan_script):
                return {"error": f"scan.sh not found at {scan_script}"}, 404
            
            # Reset the scan status
            if "SCAN_FILE" in app.config:
                with open(app.config["SCAN_FILE"], "w") as f:
                    f.write("0 Starting new scan...\n")
            
            # Reset the internal scan finished flag
            app._INT_SCAN_FINISHED = False
            
            # Launch the scan script in the background
            subprocess.Popen(
                [scan_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True
            )
            
            return {"status": "success", "message": "Scan triggered successfully"}, 200
            
        except Exception as e:
            return {"error": f"Failed to trigger scan: {str(e)}"}, 500
