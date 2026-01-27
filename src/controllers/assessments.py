# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Savoir-faire Linux, Inc.
# SPDX-License-Identifier: GPL-3.0-only

from ..models.assessment import VulnAssessment
from ..models.vulnerability import Vulnerability
from ..models.package import Package
from ..database import db
from typing import Optional


class AssessmentsController:
    """
    A class to handle a list of assessments, de-duplicating them and handling low-level stuff.
    Assessments can be added, removed, retrieved and exported or imported as dictionaries.
    """

    def __init__(self, pkgCtrl, vulnCtrl):
        """
        Take an instance of PackagesController and VulnerabilitiesController.
        They are used to resolve package and vulnerabilities by their id.
        """
        self.packagesCtrl = pkgCtrl
        self.vulnerabilitiesCtrl = vulnCtrl

    def get_by_id(self, assess_id: str) -> Optional[VulnAssessment]:
        """Return an assessment by id (str) or None if not found."""
        return VulnAssessment.query.filter_by(id=assess_id).first()

    def gets_by_vuln(self, vuln_id) -> list:
        """Return a list of assessments by vulnerability id (str) or Vulnerability instance."""
        if isinstance(vuln_id, str):
            return VulnAssessment.query.filter_by(vuln_id=vuln_id).all()
        if isinstance(vuln_id, Vulnerability):
            return VulnAssessment.query.filter_by(vuln_id=vuln_id.id).all()
        return []

    def gets_by_pkg(self, pkg_id) -> list:
        """Return a list of assessments by package id (str) or Package instance."""
        pkg_str = pkg_id if isinstance(pkg_id, str) else (pkg_id.id if isinstance(pkg_id, Package) else None)
        if pkg_str is None:
            return []
        # Filter assessments where packages JSON array contains the package id
        return [a for a in VulnAssessment.query.all() if pkg_str in a.packages]

    def gets_by_vuln_pkg(self, vuln_id, pkg_id) -> list:
        """Return a list of assessments by vulnerability id (str) and package id (str)."""
        vuln_str = vuln_id if isinstance(vuln_id, str) else vuln_id.id
        pkg_str = pkg_id if isinstance(pkg_id, str) else pkg_id.id
        return [a for a in VulnAssessment.query.filter_by(vuln_id=vuln_str).all() if pkg_str in a.packages]

    def add(self, assessment: VulnAssessment):
        """Add an assessment to the list, merging it with an existing one if present."""
        if assessment is None:
            return
        existing = VulnAssessment.query.filter_by(id=assessment.id).first()
        if existing is None:
            db.session.add(assessment)
            db.session.commit()
        else:
            existing.merge(assessment)
            db.session.commit()

    def remove(self, assess_id: str) -> bool:
        """Remove an assessment by id (str) and return True if removed, False if not found."""
        assessment = VulnAssessment.query.filter_by(id=assess_id).first()
        if assessment:
            db.session.delete(assessment)
            db.session.commit()
            return True
        return False

    def to_dict(self) -> dict:
        """Return a dictionary representation of the assessments."""
        all_assessments = VulnAssessment.query.all()
        return {a.id: a.to_dict() for a in all_assessments}

    @staticmethod
    def from_dict(pkgCtrl, vulnCtrl, data: dict):
        """Return a new instance of AssessmentsController from a dictionary."""
        item = AssessmentsController(pkgCtrl, vulnCtrl)
        for k, v in data.items():
            assessment = VulnAssessment.from_dict(v)
            existing = VulnAssessment.query.filter_by(id=assessment.id).first()
            if existing is None:
                db.session.add(assessment)
            else:
                existing.merge(assessment)
        db.session.commit()
        return item

    def __contains__(self, item) -> bool:
        """Check if an item (str or VulnAssessment) is in the list of assessments."""
        if isinstance(item, str):
            return VulnAssessment.query.filter_by(id=item).first() is not None
        elif isinstance(item, VulnAssessment):
            return VulnAssessment.query.filter_by(id=item.id).first() is not None
        return False

    def __len__(self) -> int:
        """Return the number of assessments in the list."""
        return VulnAssessment.query.count()

    def __iter__(self):
        """Allow iteration over the list of assessments."""
        return iter(VulnAssessment.query.all())
